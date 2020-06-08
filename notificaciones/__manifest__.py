# -*- coding: utf-8 -*-
{
    'name': "GeProMi Notificaciones",

    'summary': """
        Guarda plazos de avisos asociados a Expedientes""",

    'description': """
        Al crear un evento el mismo puede tener 4 estados:
            borrador, activo, vencido o cumplido:
            Borrador: Puede modificarse
            Activo: el mmismo no puede ser modificado por nadie
            Vencido: El plazo se encuentra vencido y se disparan los alertas configurados para que los usuarios realicen acciones.
            Cumplido: El evento se marca como cumpido e inmediatamente se cancela el disparo de alertas en la fecha de vencimiento.
        Notificar a los usuarios mediante pop up de sistema asociados al tipo de alerta.
        Proximas mejoras: Envio de alertas por mail.
    """,

    'author': "GIS Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Notificaciones',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['tarea', 'expediente', 'hr'],

    # always loaded
    'data': [
        'security/notificaciones_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/views_tarea.xml',
        'views/views_tarea_over.xml',
        'views/views_feriados.xml',
        'views/views_plazos.xml',
        'views/views_over.xml',
        # 'views/views_popup.xml',
        'data/auto_server.xml',
        'data/ini.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
}