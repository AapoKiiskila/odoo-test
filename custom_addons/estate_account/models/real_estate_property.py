from odoo import Command, models

class RealEstateProperty(models.Model):
	_inherit = 'real.estate.property'

	def action_set_sold(self):
		for record in self:
			self.env['account.move'].create(
				{
					'partner_id': record.buyer_id.id,
					'move_type': 'out_invoice',
					'invoice_line_ids': [
						Command.create({
							'name': '6% of the selling price',
							'quantity': 1,
							'price_unit': record.selling_price * 0.06
						}),
						Command.create({
							'name': 'Administrative fees',
							'quantity': 1,
							'price_unit': 100
						}),
					]
				}
			)

		return super().action_set_sold()