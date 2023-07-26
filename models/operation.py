from odoo import fields, models, api


class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _log_access = False
    _rec_name = "operation_name"
    _order="sequence,id"

    operation_name = fields.Char(
        string="Name"
    )

    doctor_id = fields.Many2one(
        comodel_name="res.users",
        string="Doctor"
    )
    
    reference_record=fields.Reference(
        selection=[("hospital.appointment","Appointment"),
                   ("hospital.patient","Patient")],
        string="Record"   
    )

    sequence = fields.Integer(
        default=10,
    )

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
