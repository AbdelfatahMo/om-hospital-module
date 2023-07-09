# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",

    'summary': "Hospital management system",

    'description': "Take care about pationts,staff data",

    'author': "Obadoo",
    'website': "abdelfatah_mohamed@w-ist.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management/Hospital',
    'version': '15.0.0.0',
    "license": "AGPL-3",
    'sequence': 1,
    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/patient_view.xml',
        'views/female_patient.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/appointment.xml',
        'views/patient_tag.xml',
        'views/hospital_menu.xml',
        'report/patient_card_template.xml',
        'report/patient_details_template.xml',
        'report/report.xml',
    ],

    'application': True,
    'installable': True,
    'auto_install': False,

}
