# -*- coding: utf-8 -*-

from odoo import models, fields, api


class bugTag(models.Model):
    _name = 'bm.bug.tag'
    _description = 'bug标示'
    name = fields.Char(string='名称')
    bug_ids = fields.Many2many('bm.bug',string='bug')

# class bug-management-advanced(models.Model):
#     _name = 'bug-management-advanced.bug-management-advanced'
#     _description = 'bug-management-advanced.bug-management-advanced'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
