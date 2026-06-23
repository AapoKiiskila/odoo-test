from odoo import fields, models

class RealEstatePropertyType(models.Model):
    _name = "real.estate.property.type"
    _description = "Test Model 2"

    name = fields.Char(required=True)