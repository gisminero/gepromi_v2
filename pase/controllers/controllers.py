# -*- coding: utf-8 -*-
from odoo import http

# class Pase(http.Controller):
#     @http.route('/pase/pase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pase/pase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pase.listing', {
#             'root': '/pase/pase',
#             'objects': http.request.env['pase.pase'].search([]),
#         })

#     @http.route('/pase/pase/objects/<model("pase.pase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pase.object', {
#             'object': obj
#         })