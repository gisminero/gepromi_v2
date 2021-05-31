# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Base",

    'summary': """
        Modulo base de la aplicacion
        Gestion de Procedimientos Mineros""",

    'description': """
        EL proposito del modulo base es el de establecer
        codigos y configuraciones basica.
        Todos los modulos que componen la App GeProMi,
        deberan depender de este modulo
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/gepromi_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}