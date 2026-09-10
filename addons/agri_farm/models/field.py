from odoo import fields, models


class AgriField(models.Model):
    _name = 'agri.field'
    _description = 'Farm Field'

    name = fields.Char(string='Field Name', required=True)
    farm_id = fields.Many2one(
        'agri.farm', string='Farm', required=True, ondelete='cascade'
    )
    size_hectares = fields.Float(string='Size (Hectares)')
    soil_type = fields.Selection(
        [
            ('loamy', 'Loamy'),
            ('clay', 'Clay'),
            ('sandy', 'Sandy'),
            ('silty', 'Silty'),
            ('peaty', 'Peaty'),
            ('chalky', 'Chalky'),
        ],
        string='Soil Type',
    )
    active = fields.Boolean(default=True)
