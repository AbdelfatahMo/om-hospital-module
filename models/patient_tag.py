from odoo import fields,api,models,_


class PatientTag(models.Model):
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    _sql_constraints = [
        ("unique_tag_name","unique(name)","Tag name must be unique!"),
        ("check_sequence","check(sequence > 0)","Sequence must be greater than zero!")
        ]
    
    name = fields.Char(
        string='Name',
        required=True,
    )
    sequence= fields.Integer(default=1)
    
    active = fields.Boolean(default=True)
    color = fields.Integer()
    color_2= fields.Char(string="Color 2")
    
    @api.returns('self',lambda value:value.id)
    def copy(self, default=None):
        if default is None:
            default={}
        default['name']=_("%s (copy)",self.name)
        default['sequence']=10 
        return super(PatientTag,self).copy(default)