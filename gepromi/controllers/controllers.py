# -*- coding: utf-8 -*-
from odoo import http

# class Gepromi(http.Controller):
#     @http.route('/gepromi/gepromi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gepromi/gepromi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gepromi.listing', {
#             'root': '/gepromi/gepromi',
#             'objects': http.request.env['gepromi.gepromi'].search([]),
#         })

#     @http.route('/gepromi/gepromi/objects/<model("gepromi.gepromi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gepromi.object', {
#             'object': obj
#         })