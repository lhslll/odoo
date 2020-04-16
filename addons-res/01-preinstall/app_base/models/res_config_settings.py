# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_sale_partner_only_customer = fields.Boolean("Show only customer in Sale", implied_group='app_base.group_sale_partner_only_customer')
    group_purchase_partner_only_supplier = fields.Boolean("Show only supplier in Purchase", implied_group='app_base.group_purchase_partner_only_supplier')
