# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Pases de Expedientes",

    'summary': """
        Gestionar los pases de expedientes entre oficinas""",

    'description': """
        Gestionar los pases de expedientes entre oficinas
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['gepromi', 'base', 'hr', 'expediente'],

    # always loaded
    'data': [
        'security/pase_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    #'application': True,
    'auto_install': True,
}