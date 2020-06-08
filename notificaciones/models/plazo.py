# -*- coding: utf-8 -*-

from odoo import models, fields, api


class grupo(models.Model):
    _name = 'grupo'
    name = fields.Char('Nombre', required=True)
    #user_notificar_id = fields.Many2many('res.users', string='Usuario de Grupo', required=False, readonly=False)
    user_notificar_id = fields.Many2many('hr.employee', string='Usuario de Grupo', required=False, readonly=False)

class plazo(models.Model):
    _name = 'tarea.plazo'
    _inherit = 'tarea.plazo'

    def default_user_id(self):
        return self.env.context.get("default_user_id", self.env.user)

    grupos_notificar = fields.Many2many('grupo', string='Grupos de Usuarios a Notificar',
                        required=False, readonly=False)




#PARA ACTIVARLO DESDE PANTALLA UTILIZAR ESTE BOTON
#<button string="Probar PopUp" class="oe_highlight" name="aviso" type="object"/>
#FIN PARA ACTIVARLO

