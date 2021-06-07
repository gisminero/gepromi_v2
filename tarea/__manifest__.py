# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Tarea",
    'summary': """
        Describe cada tarea de del flujo de tareas,
        perteneciente a los Procedimientos Mineros.
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
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 'gepromi', 'procedimiento', 'estado_legal'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        #'views/menu.xml',
        'views/views.xml',
        #'views/templates.xml',
        #'data/tarea_default.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}