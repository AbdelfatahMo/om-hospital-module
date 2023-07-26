from odoo import api, fields, models


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one(
        comodel_name='product.product',
    )

    unit_price = fields.Float(
        string="Unit Price",
        related='product_id.list_price',
        readonly=True,
        store=True

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

    total = fields.Float(
        string='Total',
        compute='_compute_total',
        readonly=True,
        store=True
    )

    @api.depends('unit_price', 'quantity')
    def _compute_total(self):
        if self.unit_price and self.quantity:
            for record in self:
                record.total = self.quantity*self.unit_price
        else :
            self.total=0
