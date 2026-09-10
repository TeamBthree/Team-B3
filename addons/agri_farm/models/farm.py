from odoo import fields, models


class AgriFarm(models.Model):
    _name = 'agri.farm'
    _description = 'Farm'

    name = fields.Char(string='Farm Name', required=True)
    location = fields.Char(string='Location')
    owner_id = fields.Many2one('res.partner', string='Owner')
    size_hectares = fields.Float(string='Size (Hectares)')
    field_ids = fields.One2many('agri.field', 'farm_id', string='Fields')
    field_count = fields.Integer(
        string='Field Count', compute='_compute_field_count'
    )

    def _compute_field_count(self):
        for farm in self:
            farm.field_count = len(farm.field_ids)
