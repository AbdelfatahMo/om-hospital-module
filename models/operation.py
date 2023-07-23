from odoo import fields, models, api

class HospitalOperation(models.Model):
    _name = 'hospital.operation'
    _description = 'Hospital Operation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _log_access = False

    doctor_id = fields.Many2one(
        comodel_name="res.users",
        string="Doctor"
    )
 