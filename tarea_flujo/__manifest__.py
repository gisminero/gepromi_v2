# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Flujo de Tareas 2",
    'summary': """
        Incorpora utilidades para la creacion de un flujo de
        de tareas para cada procedimiento minero.""",

    'description': """
        Tareas pertencientes a los procedimientos Mineros
    """,

    'author': "GIS Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '2.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gepromi', 'procedimiento', 'estado_legal', 'tarea','sh_message'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        ##'views/menu.xml',
        'views/views.xml',
        #'views/templates.xml',
        #'data/tarea_default.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
}