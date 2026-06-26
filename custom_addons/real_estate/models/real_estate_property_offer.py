from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class RealEstatePropertyOffer(models.Model):
    _name = "real.estate.property.offer"
    _description = "Test Model 3"
    _order = 'price desc'

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
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price of an offer must be greater than 0.'),
    ]

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

    @api.model
    def create(self, vals):
        property = self.env['real.estate.property'].browse(vals['property_id'])

        offers = self.search([('property_id', '=', property.id)])

        if offers:
            highest_offer = max(offers.mapped('price'))

            if vals['price'] < highest_offer:
                raise UserError('New offer cannot be lower than the current highest offer.')
    
        property.state = 'offer_received'

        return super().create(vals)
    
    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'