# -*- coding: utf-8 -*-

from odoo import models, fields, api

class feriados(models.Model):
    _name = 'feriados'
    _order = "fecha desc"

    name = fields.Char('Nombre', required=True, readonly=True)
    fecha = fields.Date('Fecha', readonly=True, required=True)
    state = fields.Selection([('draft', 'Borrador'), ('active', 'Activo'),], string='Estado', required=True, default="draft",
        help="Determina el estado del expediente")

    def activar(self):
        active_id = self.env.context.get('id_activo')
        feriado_obj = self.browse([active_id])
        feriado_obj.write({'state': "active"})
        return True