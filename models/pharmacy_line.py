from odoo import api, fields, models


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one(
        comodel_name='product.product',
        required=True,
    )

    unit_price = fields.Float(
        string="Unit Price",
        related='product_id.list_price',
    )

    quantity = fields.Integer(
        string="Quantity",
        required=True,
        default=0
    )

    appointment_id = fields.Many2one(
        comodel_name="hospital.appointment",
        string='Appointment',
    )

    price_subtotal = fields.Monetary(
        string='price_subtotal',
        compute='_compute_price_subtotal',
        currency_field="currency_id",
    )

        
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related="appointment_id.currency_id",
    )

    @api.depends('quantity')
    def _compute_price_subtotal(self):
        for record in self:
            record.price_subtotal = record.quantity*record.unit_price
            
