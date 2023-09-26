from odoo import models, fields, api,_
from datetime import date
from dateutil import relativedelta
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
        allowed_cancel_days = self.env["ir.config_parameter"].get_param("om_hospital.cancel_days")
        allowed_cancel_date=self.appointment_id.booking_date+relativedelta.relativedelta(days=int(allowed_cancel_days))
        if date.today() > allowed_cancel_date:
            raise ValidationError(_("can't cancel this appointment"))
        self.appointment_id.state="cancel"
        query = """SELECT id,name FROM hospital_patient"""
        self.env.cr.execute(query)
        # or
        self._cr.execute(query)
        patients = self.env.cr.fetchall()
        # For dictionary
        patients = self.env.cr.dictfetchall()
        # Reload page to viusal changes to page
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }
        # Stop close wizard after click button
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cancel.appointment.wizard',
            'target': 'new',
            'res_id':self.id
        }
