# -*- coding: utf-8 -*-
{
    'name': "GeProMi Tenencia de Expediente por Personas",

    'summary': """
        Guiar el expediente a traves del flujo de personas dentro de una oficina.
        """,

    'description': """
        Guiar el expediente a traves del flujo de personas dentro de una oficina.
        Concretamente este modulo sirve para saber quien tiene el expediente dentro de una oficina
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gepromi', 'tarea_flujo_exp', 'expediente', 'hr'],
    # always loaded
    'data': [
        'views/views_over.xml',
        'views/views.xml',
        # 'views/views_subproc.xml',
        'security/exped_person.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
}
