# -*- coding: utf-8 -*-
# from odoo import http


# class Bug-management-advanced(http.Controller):
#     @http.route('/bug-management-advanced/bug-management-advanced/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bug-management-advanced/bug-management-advanced/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bug-management-advanced.listing', {
#             'root': '/bug-management-advanced/bug-management-advanced',
#             'objects': http.request.env['bug-management-advanced.bug-management-advanced'].search([]),
#         })

#     @http.route('/bug-management-advanced/bug-management-advanced/objects/<model("bug-management-advanced.bug-management-advanced"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bug-management-advanced.object', {
#             'object': obj
#         })
