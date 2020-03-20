# -*- coding: utf-8 -*-

from odoo import models, fields, api


class bugStage(models.Model):
    _name = 'bm.bug.stage'
    _description = 'bug阶段'
    _order = 'sequence,name'
    name = fields.Char(string='名称')
    desc_detail = fields.Text(string='描述')
    status = fields.Selection([('waiting','未开始'),('doing','进行中'),('rework','重测未通过')])
    document = fields.Html(string='文档')
    sequence = fields.Integer(string='Sequence')
    percent_pro = fields.Float('进度',(3,2))
    deadline = fields.Date(string='最晚解决日期')
    create_on = fields.Datetime('创建时间',default=lambda  self:fields.Datetime.now())
    delay = fields.Boolean(string='是否延误')
    image = fields.Binary(string='图片')
    bug_ids = fields.One2many('bm.bug','stage_id',string='bug')


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
