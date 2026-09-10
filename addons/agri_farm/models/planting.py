from odoo import api, fields, models


class AgriPlanting(models.Model):
    _name = 'agri.planting'
    _description = 'Planting Cycle'
    _order = 'planting_date desc'

    name = fields.Char(
        string='Reference', required=True, default='New Planting'
    )
    field_id = fields.Many2one('agri.field', string='Field', required=True)
    crop_id = fields.Many2one('agri.crop', string='Crop', required=True)
    planting_date = fields.Date(string='Planting Date', required=True)
    expected_harvest_date = fields.Date(
        string='Expected Harvest Date', compute='_compute_expected_harvest',
        store=True, readonly=False,
    )
    quantity_planted = fields.Float(string='Quantity/Area Planted')
    state = fields.Selection(
        [
            ('planned', 'Planned'),
            ('growing', 'Growing'),
            ('harvested', 'Harvested'),
            ('failed', 'Failed'),
        ],
        string='Status', default='planned', required=True,
    )
    activity_ids = fields.One2many(
        'agri.activity', 'planting_id', string='Farm Activities'
    )
    harvest_ids = fields.One2many(
        'agri.harvest', 'planting_id', string='Harvests'
    )
    notes = fields.Text(string='Notes')

    @api.depends('planting_date', 'crop_id', 'crop_id.growth_days')
    def _compute_expected_harvest(self):
        for rec in self:
            if rec.planting_date and rec.crop_id and rec.crop_id.growth_days:
                rec.expected_harvest_date = fields.Date.add(
                    rec.planting_date, days=rec.crop_id.growth_days
                )
            elif not rec.expected_harvest_date:
                rec.expected_harvest_date = False
