# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Administración de Envios y Pases",

    'summary': """
        Funcionalidad de Administracion y Correccion de Envios.""",

    'description': """
        Permite realizar la correccion de envios erroneos y tambien la administracion de 
        envios por parte de usuarios con permisos especiales.
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente', 'sh_message', 'pase', 'tarea_flujo_exp'],
    # always loaded
    'data': [
        'security/envios_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/exp_correcc_flujo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}