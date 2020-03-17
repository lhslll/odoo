# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from lxml import etree

from odoo import api, fields, models, _


class Company(models.Model):
    _inherit = 'res.company'

    city_id = fields.Many2one('res.city', string='City of Address', compute='_compute_address', inverse='_inverse_city')
    country_enforce_cities = fields.Boolean(related="partner_id.country_id.enforce_cities")
    l10n_cn_district_id = fields.Many2one('l10n_cn.res.city.district', compute='_compute_address', inverse='_inverse_l10n_cn_district')
    l10n_cn_town_id = fields.Many2one('l10n_cn.res.city.town', compute='_compute_address', inverse='_inverse_l10n_cn_town')
    country_code = fields.Char(related='partner_id.country_id.code')

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(Company, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form' and self.env.user.lang == 'zh_CN':
            doc = etree.fromstring(res['arch'])
            replacement_xml = """
                <div class="o_address_format o_address_cn">
                    <field name="country_enforce_cities" invisible="1"/>
                    <field name="country_code" invisible="1"/>
                    <field name="country_id" class="o_address_country" placeholder="%(placeholder_country)s" options='{"no_open": True, "no_create": True}'/>
                    <field name="state_id" class="o_address_state" placeholder="%(placeholder_state)s"
                        domain="[('country_id','=', country_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{'invisible': [('country_code', 'in', ('HK', 'MO', 'TW'))]}"
                    />
                    <field name="city"  class="o_address_city" placeholder="%(placeholder_city)s"
                        attrs="{'invisible': [('country_enforce_cities', '=', True)]}"
                    />
                    <field name="city_id" class="o_address_city" placeholder="%(placeholder_city)s"
                        domain="['&amp;', ('country_id', '=', country_id), ('state_id', '=', state_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{'invisible': [('country_enforce_cities', '=', False)]}"
                    />
                    <field name="l10n_cn_district_id" class="o_address_cn_district" placeholder="%(placeholder_district)s"
                        domain="[('city_id','=', city_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{'invisible': [('country_code', '!=', 'CN')]}"
                    />
                    <field name="l10n_cn_town_id" class="o_address_cn_town" placeholder="%(placeholder_town)s"
                        domain="['&amp;', ('city_id', '=', city_id), ('district_id', '=', l10n_cn_district_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{'invisible': [('country_code', '!=', 'CN')]}"
                    />
                    <field name="street" class="o_address_street" placeholder="%(placeholder_street)s"/>
                    <field name="street2" class="o_address_street" placeholder="%(placeholder_street2)s"
                        attrs="{'invisible': [('country_code', '=', 'CN')]}"
                    />
                    <field name="zip" class="o_address_zip" placeholder="%(placeholder_zip)s"/>
                </div>
            """
            replacement_data = {
                'placeholder_country': _('Country'),
                'placeholder_state': _('Province'),
                'placeholder_city': _('City'),
                'placeholder_district': _('District/County'),
                'placeholder_town': _('Town/Street'),
                'placeholder_street': _('Detailed Street...'),
                'placeholder_street2': _('Street 2...'),
                'placeholder_zip': _('ZIP'),
            }
            replacement_formatted = replacement_xml % replacement_data
            replace_node = etree.fromstring(replacement_formatted)
            for address_node in doc.xpath("//div[hasclass('o_address_format')]"):
                address_node.getparent().replace(address_node, replace_node)
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    def _get_company_address_fields(self, partner):
        res = super(Company, self)._get_company_address_fields(partner)
        res.update({
            'city_id': partner.city_id,
            'l10n_cn_district_id': partner.l10n_cn_district_id,
            'l10n_cn_town_id': partner.l10n_cn_town_id,
        })
        return res

    def _inverse_city(self):
        for company in self:
            company.partner_id.city = company.city
            company.partner_id.city_id = company.city_id

    def _inverse_l10n_cn_district(self):
        for company in self:
            company.partner_id.l10n_cn_district_id = company.l10n_cn_district_id

    def _inverse_l10n_cn_town(self):
        for company in self:
            company.partner_id.l10n_cn_town_id = company.l10n_cn_town_id

    def on_change_country(self, country_id):
        res = super(Company, self).on_change_country(country_id)
        if country_id:
            country = self.env['res.country'].browse(country_id)
            res['value']['country_enforce_cities'] = country.enforce_cities
            res['value']['country_code'] = country.code
        return res

    @api.onchange('country_id')
    def _onchange_country_id_wrapper(self):
        """ Override """
        if self.country_id:
            if self.country_id != self.state_id.country_id:
                self.state_id = False
            if self.country_id != self.city_id.country_id:
                self.city_id = False
        res = super(Company, self)._onchange_country_id_wrapper()
        res['domain']['city_id'] = ['&', ('country_id', '=', self.country_id.id), ('state_id', '=', self.state_id.id)]
        return res

    @api.onchange('state_id')
    def _onchange_state(self):
        """ Override """
        city_domain = ['&', ('country_id', '=', self.country_id.id), ('state_id', '=', self.state_id.id)]
        if self.state_id:
            if self.state_id.country_id:
                self.country_id = self.state_id.country_id
            if self.country_code == 'CN':
                region_codes = self.partner_id._get_l10n_cn_state_codes_for_region()
                if self.state_id.code in region_codes:
                    self.country_id = self.env['res.country'].search([('code', '=', self.state_id.code)])
            if self.env['res.city'].search_count(city_domain) == 1:
                self.city_id = self.env['res.city'].search(city_domain)
            if self.state_id != self.city_id.state_id:
                self.city_id = False
        return {'domain': {'city_id': city_domain}}

    @api.onchange('city_id')
    def _onchange_city_id(self):
        district_domain = [('city_id', '=', self.city_id.id)]
        if self.city_id:
            self.city = self.city_id.name
            self.zip = self.city_id.zipcode
            if self.city_id.state_id != self.state_id or not self.state_id:
                self.state_id = self.city_id.state_id
            if self.city_id != self.l10n_cn_district_id.city_id:
                self.l10n_cn_district_id = False
        else:
            self.city = ''
            self.l10n_cn_district_id = False
        return {'domain': {'l10n_cn_district_id': district_domain}}

    @api.onchange('l10n_cn_district_id')
    def _onchange_l10n_cn_district_id(self):
        town_domain = ['&', ('city_id', '=', self.city_id.id), ('district_id', '=', self.l10n_cn_district_id.id)]
        if self.l10n_cn_district_id:
            town_domain = [('district_id', '=', self.l10n_cn_district_id.id)]
            self.zip = self.l10n_cn_district_id.zipcode or self.city_id.zipcode
            if self.l10n_cn_district_id != self.l10n_cn_town_id.district_id:
                self.l10n_cn_town_id = False
        else:
            self.l10n_cn_town_id = False
            self.zip = self.city_id.zipcode
        return {'domain': {'l10n_cn_town_id': town_domain}}
