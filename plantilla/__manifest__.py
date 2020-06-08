# -*- coding: utf-8 -*-
{
    'name': "GeProMi Plantillas",

    'summary': """
        Es posible adjuntar plantillas en las tareas con figuradas, que luego
        estaran disponibles en la pantalla Expediente.
        """,

    'description': """
        Está pensado que las plantillas se encuentren disponibles en un pop up
        que se abre desde un link cerca de el campo Ubicacion actual
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.3',

    # any module necessary for this one to work correctly
    'depends': ['base','gepromi', 'tarea', 'procedimiento', 'expediente'],
    # always loaded
    'data': [
        'views/views.xml',
        'views/views_over.xml',
        'security/plantilla_security.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
}