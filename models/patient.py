from odoo import fields, api, models, _
from datetime import date
from dateutil import relativedelta
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        copy=False,
        tracking=True,
    )

    national_id = fields.Char(
        string="National ID",
        required=True,
    )

    date_of_birth = fields.Date(
        string='Date date of birth'
    )

    ref = fields.Char(
        string='Reference',
        readonly=True,
    )

    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        inverse='_inverse__compute_age',
        search='_search_age',
        store=True,



    )
    appointment_count = fields.Integer(
        string="Appointments count",
        compute="_compute_appointment_count",
        store=True,
    )

    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female')],
        default='male',
        tracking=True,
        required=True,
    )

    image = fields.Image()
    # Contact 
    phone = fields.Char()
    email = fields.Char()
    website = fields.Char()

    note = fields.Text(
        string='Notes',
        tracking=True
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        tracking=True
    )

    parent = fields.Char(
        string="Parent"
    )

    marital_state = fields.Selection(
        selection=[("married", "Married"),
                   ("single", "Single")],
        string="Marital State",
        default='single',
        track=True,
        required=True,
    )

    partner_name = fields.Char(
        string="Partner Name",
    )

    appointment_ids = fields.One2many(
        string="Appointments",
        comodel_name="hospital.appointment",
        inverse_name="patient_id"
    )

    tag_ids = fields.Many2many(
        string='Tags',
        comodel_name='patient.tag',
        relation='patient_tag_patient_rel',
        column1='patient_tag_id',
        column2='patient_id',
    )

    is_birthday = fields.Boolean(
        string="Birthday ?",
        compute='_compute_is_birthdate'
    )

    @api.depends('date_of_birth')
    def _compute_is_birthdate(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                if record.date_of_birth.day == today.day and record.date_of_birth.month == today.month:
                    record.is_birthday = True
                else:
                    record.is_birthday = False
            else:
                record.is_birthday=False
    # change record in database
    # @api.onchange('date_of_birth')
    # def _onchange_date_of_birth(self):
    #     today = date.today()
    #     if self.date_of_birth:
    #         self.age = today.year - self.date_of_birth.year - \
    #             ((today.month, today.day) <
    #              (self.date_of_birth.month, self.date_of_birth.day))

    # not save record in database

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year - \
                    ((today.month, today.day) <
                     (rec.date_of_birth.month, rec.date_of_birth.day))
            else:
                rec.age = 0

    @api.depends("age")
    def _inverse__compute_age(self):
        today = date.today()
        for record in self:
            record.date_of_birth = today - \
                relativedelta.relativedelta(years=record.age)

    # search on compute field not have store = true
    def _search_age(self, operator, value):
        today = date.today()
        birth_date = today - relativedelta.relativedelta(years=value)
        start_year = birth_date.replace(day=1, month=1)
        end_year = birth_date.replace(day=31, month=12)
        return [('birth_of_date', ">=", start_year), ("birth_of_date", "<=", end_year)]

    @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        ## Search count method
        # for record in self:
        #     record.appointment_count = self.env["hospital.appointment"].search_count(
        #         [("patient_id", "=", record.id)])
        ## Read group method
        appointment_groups=self.env["hospital.appointment"].read_group(domain=[],fields=["patient_id"],group_by=["patient_id"])
        for appointment in appointment_groups:
            print("..............", appointment)
            patient_id=appointment.get("patient_id")[0]
            patient_rec= self.browse(patient_id)
            patient_rec.appointment_count=appointment.get("patient_id_count")
            self-=patient_rec
        self.appointment_count=0
    # Overrode create method from Model

    @api.constrains("date_of_birth")
    def _ckeck_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Enter Valid date!"))

    @api.constrains("national_id")
    def _check_national_id(self):
        for record in self:
            if len(record.national_id) != 14:
                raise ValidationError(_("Enter valid National ID"))
            elif self.search_count([("national_id", "=", record.national_id)]) > 1:
                raise ValidationError(_("This National ID is used"))

    @api.ondelete(at_uninstall=False)
    def _chech_appointments(self):
        for record in self:
            if record.appointment_ids:
                raise ValidationError(
                    _("Can't delete patient has Appointments."))

    @api.model
    def create(self, vals):
        vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref:
            vals["ref"] = self.env["ir.sequence"].next_by_code(
                "hospital.patient")
        return super(HospitalPatient, self).write(vals)

    # override name_get on Model to return name + ref
    # instead of _rec_name = 'name' returns name only

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]

    def action_view_appointment(self):
        return {
            'name':_('Appointments'),
            'res_model':'hospital.appointment',
            'view_mode':'list,form',
            'context':{'default_patient_id':self.id},
            'domain':[('patient_id','=',self.id)],
            'target':'current',
            'type':'ir.actions.act_window'
        }