from odoo import api, fields, models

class RealEstatePropertyType(models.Model):
    _name = "real.estate.property.type"
    _description = "Test Model 2"
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence')

    offer_count = fields.Integer(compute='_compute_offer_count')

    property_ids = fields.One2many('real.estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('real.estate.property.offer', 'property_type_id', string='Offers')

    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'Type must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
