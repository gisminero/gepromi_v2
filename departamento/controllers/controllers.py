# -*- coding: utf-8 -*-
from odoo import http

# class Departamento(http.Controller):
#     @http.route('/departamento/departamento/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/departamento/departamento/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('departamento.listing', {
#             'root': '/departamento/departamento',
#             'objects': http.request.env['departamento.departamento'].search([]),
#         })

#     @http.route('/departamento/departamento/objects/<model("departamento.departamento"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('departamento.object', {
#             'object': obj
#         })