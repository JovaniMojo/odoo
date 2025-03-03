# -*- coding: utf-8 -*-
# from odoo import http


# class Carppoling2(http.Controller):
#     @http.route('/carppoling2/carppoling2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/carppoling2/carppoling2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('carppoling2.listing', {
#             'root': '/carppoling2/carppoling2',
#             'objects': http.request.env['carppoling2.carppoling2'].search([]),
#         })

#     @http.route('/carppoling2/carppoling2/objects/<model("carppoling2.carppoling2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('carppoling2.object', {
#             'object': obj
#         })

