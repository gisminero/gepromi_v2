# -*- coding: utf-8 -*-
{
    'name': "GeProMi Documentacion Digital",

    'summary': """
        La Documentacion Digital será soporte para el
        Expediente Digital.
        """,

    'description': """
        Este archivo tiene la funcion de brindar soporte para el expediente digital.
        Se destacan las siguientes funciones:
        * Soporte para documento adjunto, el cual debe mostrarse de alguna manera en el cuerpo del expediente.
        * Soporte para añadir archivo al documento adjunto. Para lo cual se deberan poder unir archivos PDF, sean firmados digitalmente o no.
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gepromi', 'expediente', 'hr', 'tarea_flujo_exp', 'web'],
    #, 'tarea_flujo_exp'
    # always loaded
    'data': [
        'views/views_over.xml',
        'views/views.xml',
        'security/doc_digital.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
}
