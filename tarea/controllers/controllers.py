# -*- coding: utf-8 -*-
from odoo import http

# class Tarea(http.Controller):
#     @http.route('/tarea/tarea/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tarea/tarea/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tarea.listing', {
#             'root': '/tarea/tarea',
#             'objects': http.request.env['tarea.tarea'].search([]),
#         })

#     @http.route('/tarea/tarea/objects/<model("tarea.tarea"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tarea.object', {
#             'object': obj
#         })