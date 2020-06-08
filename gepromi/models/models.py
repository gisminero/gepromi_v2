# -*- coding: utf-8 -*-

from odoo import models, fields, api

class gepromi(models.Model):
    _name = 'gepromi.gepromi'

    name = fields.Char()
    value = fields.Integer()
    #value2 = fields.Float(compute="_value_pc", store=True)
    #description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


#class mineral(models.Model):
    #_name = 'mineral'

    #name = fields.Char('Nombre', required=True)
    #categoria = fields.Selection([
        #('Primera', 'Primera'),
        #('Segunda', 'Segunda'),
        #('Tercera', 'Tercera'),], required=True,
        #help="Categoria del mineral")
    #active = fields.Boolean('Activo', default=True)