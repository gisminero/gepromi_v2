# -*- coding: utf-8 -*-

from odoo import models, fields, api

class departamento(models.Model):
    _name = 'departamento.departamento'
    name = fields.Char('Nombre', required=True)
    description = fields.Char('Descripcion', required=False)
    state_id = fields.Many2one('res.country.state', string="Provincia")
    active = fields.Boolean('Activo', default=True)

# class departamento(models.Model):
#     _name = 'departamento.departamento'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100