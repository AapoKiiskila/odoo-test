from odoo import fields, models

class RealEstatePropertyTag(models.Model):
    _name = "real.estate.property.tag"
    _description = "Test Model 4"
    _order = 'name'

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'Tag must be unique.'),
    ]