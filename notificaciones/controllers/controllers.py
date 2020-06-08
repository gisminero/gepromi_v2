# -*- coding: utf-8 -*-
from odoo import http

# class Procedimiento(http.Controller):
#     @http.route('/procedimiento/procedimiento/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/procedimiento/procedimiento/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('procedimiento.listing', {
#             'root': '/procedimiento/procedimiento',
#             'objects': http.request.env['procedimiento.procedimiento'].search([]),
#         })

#     @http.route('/procedimiento/procedimiento/objects/<model("procedimiento.procedimiento"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('procedimiento.object', {
#             'object': obj
#         })