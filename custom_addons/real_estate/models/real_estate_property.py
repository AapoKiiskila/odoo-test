from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'Test Model'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + timedelta(days=90), string='Available From')
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[('new', 'New'),
                   ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='new',
        string='Status'
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price')

    property_type_id = fields.Many2one('real.estate.property.type', string='Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('real.estate.property.tag', string='Tags')
    offer_ids = fields.One2many('real.estate.property.offer', 'property_id', string='Offers')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.00

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled properites cannot be sold.')
            record.state = 'sold'

    def action_set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold properites cannot be canceled.')
            record.state = 'canceled'