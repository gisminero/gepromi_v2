# -*- coding: utf-8 -*-

from odoo import models, fields, api

class estado_legal(models.Model):
    _name = 'estado_legal.estado_legal'

    name = fields.Char('Nombre', required=True)
    description = fields.Char('Descripcion', required=True)
    active = fields.Boolean('Activo', default=True)
    
    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100
