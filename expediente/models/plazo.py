# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mineral(models.Model):
    _name = 'mineral'

    name = fields.Char('Nombre', required=True)
    categoria = fields.Selection([
        ('Primera', 'Primera'),
        ('Segunda', 'Segunda'),
        ('Tercera', 'Tercera'),], required=True,
        help="Categoria del mineral")
    active = fields.Boolean('Activo', default=True)

#
# from odoo import models, fields
#
# class Procedimiento(models.Model):
#     _name = 'procedimiento.procedimiento'
#     _description = 'procedimiento GMN'
#     name = fields.Char('Nombre', required=True)
#     description = fields.Char('Description', required=True)
