# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_l10n_cn_localize_amap = fields.Boolean("Amap Cities Data")
