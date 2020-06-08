# -*- coding: utf-8 -*-
from odoo import http

# class Expediente(http.Controller):
#     @http.route('/expediente/expediente/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expediente/expediente/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expediente.listing', {
#             'root': '/expediente/expediente',
#             'objects': http.request.env['expediente.expediente'].search([]),
#         })

#     @http.route('/expediente/expediente/objects/<model("expediente.expediente"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expediente.object', {
#             'object': obj
#         })