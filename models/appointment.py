from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):

    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ["mail.thread", 'mail.activity.mixin']

    _rec_name = "sequence"

    sequence = fields.Char()

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        ondelete='set null'
    )

    gender = fields.Selection(
        string='Gender',
        related='patient_id.gender',
        readonly=True
    )

    ref = fields.Char(
        string='Reference',
        tracking=True,
        readonly=True,
    )

    prescription = fields.Html(
        string="Prescription",
    )

    appointment_time = fields.Datetime(
        string='Appointment Time'
    )

    booking_date = fields.Date(
        string='Booking Date',
        default=fields.Date.context_today,
    )

    last_borrow_date = fields.Datetime(
        "Last Borrowed On",
        default=lambda self: fields.Datetime.now(),
    )

    priority = fields.Selection(
        selection=[('0', 'Very Low'),
                   ('1', 'Low'),
                   ('2', 'Normal'),
                   ('3', 'High')],
        string='Priority',
        default='0'

    )

    state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('in_consultation', 'In Consultation'),
                   ('done', 'Done'),
                   ('cancel', 'Cancel')],
        string="Status",
        default='draft'
    )

    doctor_id = fields.Many2one(
        comodel_name='res.users',
        string='Doctor',
    )

    operation_id = fields.Many2one(
        comodel_name="hospital.operation",
        string="Operation"
    )

    pharmacy_lines_ids = fields.One2many(
        string='Medicine',
        comodel_name='appointment.pharmacy.lines',
        inverse_name='appointment_id',
    )

    hide_sales_price = fields.Boolean()

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.ref = self.patient_id.ref

    def do_action(self):
        return {
            'effect': {
                'fadeout': 'slow',  # to disappear automaticly
                'message': "Done",  # message to put
                # 'image': 'path', #to show custom image
                'type': 'rainbow_man',
            }
        }

    @api.model
    def create(self, values):
        result = super(HospitalAppointment, self)
        values["sequence"] = self.env["ir.sequence"].next_by_code(
            "hospital.appointment")
        return result.create(values)

    def write(self, values):
        res = super(HospitalAppointment, self)
        if not self.sequence:
            values["sequence"] = self.env["ir.sequence"].next_by_code(
                "hospital.appointment")
        return res.write(values)

    def unlink(self):
        for record in self:
            if record.state not in ("draft", "cancel"):
                raise ValidationError(_("Can only delete drafted Records"))
        return super(HospitalAppointment, self).unlink()

    def action_in_consultation(self):
        if self.state == 'draft':
            self.state = 'in_consultation'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        action = self.env.ref(
            "om_hospital.cancel_appointment_action").read()[0]
        return action

    def action_done(self):
        self.state = 'done'
