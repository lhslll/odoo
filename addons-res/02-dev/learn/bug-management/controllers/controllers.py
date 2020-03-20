# -*- coding: utf-8 -*-
from odoo import http

class Bug(http.Controller):
    @http.route('/bug-management')
    def BugManagement(self,**kwargs):
        bugs=http.request.env['bm.bug']
        domain_bug=[('is_closed','=',False)]
        bugs_open=bugs.search(domain_bug)
        return http.request.render('bug-management.bugs_template',{'bugs_open':bugs_open})


# class Bug-management(http.Controller):
#     @http.route('/bug-management/bug-management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bug-management/bug-management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bug-management.listing', {
#             'root': '/bug-management/bug-management',
#             'objects': http.request.env['bug-management.bug-management'].search([]),
#         })

#     @http.route('/bug-management/bug-management/objects/<model("bug-management.bug-management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bug-management.object', {
#             'object': obj
#         })
