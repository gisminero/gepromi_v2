# -*- coding: utf-8 -*-
from odoo import http

# class EstadoLegal(http.Controller):
#     @http.route('/estado_legal/estado_legal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estado_legal/estado_legal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('estado_legal.listing', {
#             'root': '/estado_legal/estado_legal',
#             'objects': http.request.env['estado_legal.estado_legal'].search([]),
#         })

#     @http.route('/estado_legal/estado_legal/objects/<model("estado_legal.estado_legal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estado_legal.object', {
#             'object': obj
#         })