from odoo import fields, models

class RealEstatePropertyTag(models.Model):
    _name = "real.estate.property.tag"
    _description = "Test Model 4"

    name = fields.Char(required=True)