from odoo import fields, models


class AgriActivity(models.Model):
    _name = 'agri.activity'
    _description = 'Farm Activity / Growth Log'
    _order = 'date desc'

    planting_id = fields.Many2one(
        'agri.planting', string='Planting', required=True, ondelete='cascade'
    )
    activity_type = fields.Selection(
        [
            ('watering', 'Watering'),
            ('fertilizer', 'Fertilizer'),
            ('pest_control', 'Pest Control'),
            ('weeding', 'Weeding'),
            ('pruning', 'Pruning'),
            ('other', 'Other'),
        ],
        string='Activity Type', required=True,
    )
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    notes = fields.Text(string='Notes')
