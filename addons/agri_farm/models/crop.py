from odoo import fields, models


class AgriCrop(models.Model):
    _name = 'agri.crop'
    _description = 'Crop Type'

    name = fields.Char(string='Crop Name', required=True)
    growth_days = fields.Integer(
        string='Typical Growth Days',
        help='Average number of days from planting to harvest.',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Linked Product',
        help='The sellable/stockable product this crop becomes once harvested '
             '(links into Inventory/Sales once harvest is recorded).',
    )
    notes = fields.Text(string='Notes')
