# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class procedimiento(models.Model):
    _name = 'procedimiento.procedimiento'
    name = fields.Char('Nombre', required=True)
    description = fields.Char('Descripcion', required=True)
    active = fields.Boolean('Activo', default=True)
    iniciado = fields.Selection([
        ('1', 'Usuario'),
        ('2', 'Tarea')
        ], 'Iniciado por', index=True, readonly=False,required=True)
    susplazo = fields.Selection([
        ('1', 'Si'),
        ('2', 'No')
        ], 'Suspede Plazos', index=True, readonly=False,required=True, default='2')

    @api.onchange ('susplazo')
    def suspende(self):
        if self.iniciado =='1':
            self.susplazo = '2'


#            view = self.env.ref('sh_message.sh_message_wizard')
#            view_id = view and view.id or False
#            context = dict(self._context or {})
#            context['message'] = 'Los procedimientos iniciados por usuarios no suspende plazos'
#            return {
#                    'name': 'Informacion',
#                    'type': 'ir.actions.act_window',
#                    'view_type': 'form',
#                    'view_mode': 'form',
#                    'res_model': 'sh.message.wizard',
#                    'views': [(view.id, 'form')],
#                    'view_id': view.id,
#                    'target': 'new',
#                    'context': context,
#            }