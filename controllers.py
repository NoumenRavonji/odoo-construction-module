# -*- coding: utf-8 -*-
from openerp import http

# class Gent(http.Controller):
#     @http.route('/gent/gent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gent/gent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gent.listing', {
#             'root': '/gent/gent',
#             'objects': http.request.env['gent.gent'].search([]),
#         })

#     @http.route('/gent/gent/objects/<model("gent.gent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gent.object', {
#             'object': obj
#         })