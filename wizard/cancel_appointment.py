from odoo import models, fields, api,_
from datetime import date
from odoo.exceptions import ValidationError

class CancelAppointmentWizard(models.TransientModel):
    _name = 'cancel.appointment.wizard'
    _description = 'Cancel Appointment Wizard'

    # To set default values for Fields
    # Put above fields
    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res["cancel_date"] = date.today()
        print("......Contect....." + str(self.env.context.get('active_id')))
        if self.env.context.get("active_id"):
            res["appointment_id"] = self.env.context['active_id']
        return res

    appointment_id = fields.Many2one(
        comodel_name="hospital.appointment",
        string="Appointment",
        domain=[('state','=','draft'),('priority','in',('0','1'))],
    )

    reason = fields.Text()
    cancel_date = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        if self.appointment_id.booking_date==fields.Date.today():
            raise ValidationError(_("can't cancel this appointment"))
        self.appointment_id.state="cancel"
        return
