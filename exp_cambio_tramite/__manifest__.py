# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Cambio de Tramite",

    'summary': """
        Funcionalidad de Cambio de tramite en un expediente.""",

    'description': """
        Permite realizar el cambio de tramite en un expediente, cuando se cumple determinado estado legal o procesal.
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente', 'sh_message'],
    # always loaded
    'data': [
        'security/cambio_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_over.xml',
        'views/views_cambio_exp.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}