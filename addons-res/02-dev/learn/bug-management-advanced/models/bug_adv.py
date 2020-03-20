# -*- coding: utf-8 -*-

from odoo import models, fields, api


class bugAdvanced(models.Model):
    _inherit = 'bm.bug'
    need_time = fields.Integer(string='所需时间(小时)')
    name = fields.Char(help='简要描述发现的bug')
    stage_id = fields.Many2one('bm.bug.stage',string='阶段')
    tag_ids = fields.Many2many('bm.bug.tag','bug_tag_rel','bug_id','tag_id',string='标示')
    discovers = fields.Reference([('res.user','用户'),('res.partner','合作伙伴')],'bug发现者')

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
