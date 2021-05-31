# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Expediente",

    'summary': """
        Corresponde a la entidad nucleo del sistema SIGETRAMI""",

    'description': """
        Corresponde a la entidad nucleo del sistema SIGETRAMI
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gepromi', 'procedimiento', 'hr', 'departamento', 'mineral', 'estado_legal', 'sh_message'],

    # always loaded
    'data': [
        'security/expediente_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
        'models/secuence.xml',
        'reports/pases_report.xml',
        'views/popup_mas.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}
