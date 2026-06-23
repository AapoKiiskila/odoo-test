from datetime import timedelta
from odoo import api, fields, models

class RealEstatePropertyOffer(models.Model):
    _name = "real.estate.property.offer"
    _description = "Test Model 3"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'),
                   ('refused', 'Refused'),
        ],
        copy=False
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline')

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('real.estate.property', required=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days
    
    def action_accept(self):
        for record in self:
            record.status = 'accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
