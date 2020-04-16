# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re

from email.utils import formataddr

import requests
from lxml import etree
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError
from odoo.tools import pycompat


class Partner(models.Model):
    _inherit = 'res.partner'
    # 在 hooks.py 中已初始化
    def _get_default_customer(self):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        is_customer = search_partner_mode == 'customer'
        if is_customer and not self.env.context.get('default_customer'):
            return is_customer
        else:
            return None

    def _get_default_supplier(self):
        search_partner_mode = self.env.context.get('res_partner_search_mode')
        is_supplier = search_partner_mode == 'supplier'
        if is_supplier and not self.env.context.get('default_supplier'):
            return is_supplier
        else:
            return None

    customer = fields.Boolean(string='Is a Customer', default=_get_default_customer, inverse='_set_customer',
                               help="Check this box if this contact is a customer. It can be selected in sales orders.")
    supplier = fields.Boolean(string='Is a Vendor', default=_get_default_supplier, inverse='_set_supplier',
                               help="Check this box if this contact is a vendor. It can be selected in purchase orders.")

    # supplier_rank = fields.Integer(default=0)
    # customer_rank = fields.Integer(default=0)

    customer_rank_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Customer Priority")

    supplier_rank_priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Vendor Priority")


    def _set_customer(self):
        for rec in self:
            if rec.customer:
                if rec.customer_rank < 1 or not rec.customer_rank:
                    rec.customer_rank = 1
            else:
                rec.customer_rank = 0

    def _set_supplier(self):
        for rec in self:
            if rec.supplier:
                if rec.supplier_rank < 1 or not rec.supplier_rank:
                    rec.supplier_rank = 1
            else:
                rec.supplier_rank = 0


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        partner_search_mode = self.env.context.get('res_partner_search_mode')
        if self.env.user.has_group('app_base.group_sale_partner_only_customer') and partner_search_mode \
                and partner_search_mode == 'customer':
            args.append(['customer_rank', '>', 0])
        elif self.env.user.has_group('app_base.group_purchase_partner_only_supplier') and partner_search_mode \
                and partner_search_mode == 'supplier':
            args.append(['supplier_rank', '>', 0])
        else:
            pass
        return super(Partner, self)._name_search(name, args, operator, limit, name_get_uid)


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        partner_search_mode = self.env.context.get('res_partner_search_mode')
        if self.env.user.has_group('app_base.group_sale_partner_only_customer') and partner_search_mode \
                and partner_search_mode == 'customer':
            domain.append(['customer_rank', '>', 0])
        elif self.env.user.has_group('app_base.group_purchase_partner_only_supplier') and partner_search_mode \
                and partner_search_mode == 'supplier':
            domain.append(['supplier_rank', '>', 0])
        else:
            pass
        return super(Partner, self).search_read(domain, fields, offset, limit, order)
