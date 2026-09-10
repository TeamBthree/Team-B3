from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AgriHarvest(models.Model):
    _name = 'agri.harvest'
    _description = 'Harvest'
    _order = 'harvest_date desc'

    name = fields.Char(
        string='Reference', required=True, default='New Harvest'
    )
    planting_id = fields.Many2one(
        'agri.planting', string='Planting', required=True
    )
    crop_id = fields.Many2one(
        related='planting_id.crop_id', string='Crop',
        store=True, readonly=True,
    )
    field_id = fields.Many2one(
        related='planting_id.field_id', string='Field',
        store=True, readonly=True,
    )
    harvest_date = fields.Date(
        string='Harvest Date', required=True, default=fields.Date.today
    )
    quantity = fields.Float(string='Quantity Harvested', required=True)
    quality_grade = fields.Selection(
        [
            ('a', 'Grade A'),
            ('b', 'Grade B'),
            ('c', 'Grade C'),
            ('reject', 'Reject'),
        ],
        string='Quality Grade', default='a', required=True,
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed - In Stock'),
        ],
        default='draft', required=True,
    )
    lot_id = fields.Many2one(
        'stock.lot', string='Stock Lot', readonly=True, copy=False
    )
    picking_id = fields.Many2one(
        'stock.picking', string='Stock Receipt', readonly=True, copy=False
    )
    notes = fields.Text(string='Notes')

    expiration_date = fields.Datetime(
        related='lot_id.expiration_date', string='Expiration Date',
        store=True, readonly=True,
    )
    quantity_remaining = fields.Float(
        string='Quantity Remaining', compute='_compute_quantity_remaining',
        search='_search_quantity_remaining',
    )
    spoilage_status = fields.Selection(
        [
            ('not_tracked', 'Not Tracked'),
            ('cleared', 'Cleared'),
            ('fresh', 'Fresh'),
            ('at_risk', 'At Risk'),
            ('expired', 'Expired'),
        ],
        string='Spoilage Status', compute='_compute_spoilage_status',
    )
    recommended_action = fields.Char(
        string='Recommended Action', compute='_compute_spoilage_status',
    )

    def _compute_quantity_remaining(self):
        for rec in self:
            if not rec.lot_id:
                rec.quantity_remaining = 0.0
                continue
            quants = self.env['stock.quant'].search([
                ('lot_id', '=', rec.lot_id.id),
                ('location_id.usage', '=', 'internal'),
            ])
            rec.quantity_remaining = sum(quants.mapped('quantity'))

    def _search_quantity_remaining(self, operator, value):
        ops = {
            '>': lambda a, b: a > b,
            '>=': lambda a, b: a >= b,
            '<': lambda a, b: a < b,
            '<=': lambda a, b: a <= b,
            '=': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
        }
        if operator not in ops:
            raise NotImplementedError(
                'Unsupported operator for quantity_remaining search.'
            )
        candidates = self.search([
            ('state', '=', 'confirmed'), ('lot_id', '!=', False),
        ])
        matched = candidates.filtered(
            lambda h: ops[operator](h.quantity_remaining, value)
        )
        return [('id', 'in', matched.ids)]

    @api.depends(
        'lot_id.expiration_date', 'lot_id.alert_date',
        'quantity_remaining', 'state',
    )
    def _compute_spoilage_status(self):
        now = fields.Datetime.now()
        for rec in self:
            if rec.state != 'confirmed' or not rec.lot_id \
                    or not rec.lot_id.expiration_date:
                rec.spoilage_status = 'not_tracked'
                rec.recommended_action = ''
                continue

            if rec.quantity_remaining <= 0:
                rec.spoilage_status = 'cleared'
                rec.recommended_action = _(
                    'Fully sold or processed — no stock remaining. '
                    'No action needed.'
                )
                continue

            expiration = rec.lot_id.expiration_date
            alert = rec.lot_id.alert_date

            if now > expiration:
                rec.spoilage_status = 'expired'
                rec.recommended_action = _(
                    'Remove from sale — write off as waste or record spoilage.'
                )
            elif alert and now >= alert:
                rec.spoilage_status = 'at_risk'
                if rec.quantity_remaining > (rec.quantity / 2.0):
                    rec.recommended_action = _(
                        'Large quantity still on hand — process into a '
                        'value-added product or offer a discounted quick sale.'
                    )
                else:
                    rec.recommended_action = _(
                        'Small quantity remaining — sell immediately at '
                        'standard price.'
                    )
            else:
                rec.spoilage_status = 'fresh'
                rec.recommended_action = _('No action needed.')

    def action_confirm_harvest(self):
        for rec in self:
            if rec.state == 'confirmed':
                continue
            if rec.quantity <= 0:
                raise UserError(_(
                    'Quantity harvested must be greater than zero.'
                ))

            product = rec.crop_id.product_id
            if not product:
                raise UserError(_(
                    "The crop '%s' has no linked product. Set one on the "
                    "Crop before confirming a harvest."
                ) % rec.crop_id.name)

            company = self.env.company
            warehouse = self.env['stock.warehouse'].search(
                [('company_id', '=', company.id)], limit=1
            )
            if not warehouse:
                raise UserError(_(
                    'No warehouse found for this company.'
                ))

            dest_location = warehouse.lot_stock_id
            source_location = self.env['stock.location'].search(
                [('usage', '=', 'production')], limit=1
            )
            if not source_location:
                source_location = self.env['stock.location'].search(
                    [('usage', '=', 'inventory')], limit=1
                )

            lot = False
            if product.tracking in ('lot', 'serial'):
                lot_name = (
                    rec.name if rec.name != 'New Harvest'
                    else 'HARVEST-%s' % rec.harvest_date
                )
                lot = self.env['stock.lot'].create({
                    'name': lot_name,
                    'product_id': product.id,
                    'company_id': company.id,
                })

            picking = self.env['stock.picking'].create({
                'picking_type_id': warehouse.in_type_id.id,
                'location_id': source_location.id,
                'location_dest_id': dest_location.id,
                'origin': rec.name,
            })
            move = self.env['stock.move'].create({
                'product_id': product.id,
                'product_uom_qty': rec.quantity,
                'product_uom': product.uom_id.id,
                'picking_id': picking.id,
                'location_id': source_location.id,
                'location_dest_id': dest_location.id,
            })
            picking.action_confirm()
            picking.action_assign()

            move_line_vals = {'quantity': rec.quantity}
            if lot:
                move_line_vals['lot_id'] = lot.id
            if move.move_line_ids:
                move.move_line_ids.write(move_line_vals)
            else:
                move_line_vals.update({
                    'move_id': move.id,
                    'product_id': product.id,
                    'product_uom_id': product.uom_id.id,
                    'location_id': source_location.id,
                    'location_dest_id': dest_location.id,
                    'picking_id': picking.id,
                })
                self.env['stock.move.line'].create(move_line_vals)

            picking.button_validate()

            rec.write({
                'lot_id': lot.id if lot else False,
                'picking_id': picking.id,
                'state': 'confirmed',
            })
            if rec.planting_id.state != 'harvested':
                rec.planting_id.state = 'harvested'
