# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Seguimiento de Flujo de Tareas",

    'summary': """
        Guiar el expediente a traves del flujo de tareas.
        """,

    'description': """
        Recordar otorgar permisos si necesitamos que le usuario ingrese Documentos en el Flujo
        En el caso que el trámite se encuentre con flujo construido, se seguirá
        por el flujo de tareas.
        Ultima version 07-08-2019 - Solucionado el problema al ingresar documentos en el flujo
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gepromi', 'tarea_flujo', 'expediente', 'notificaciones', 'exp_cambio_tramite'],#, 'apiclient'
    # always loaded
    'data': [
        'views/views_over.xml',
        'views/views.xml',
        'views/views_subproc.xml',
        'security/tarea_security.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}
