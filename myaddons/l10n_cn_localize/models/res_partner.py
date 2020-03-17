# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from lxml import etree

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval


class Partner(models.Model):
    _inherit = ['res.partner']
    _name = 'res.partner'

    l10n_cn_district_id = fields.Many2one('l10n_cn.res.city.district', string='District/County', help='District/County are part of a city')
    l10n_cn_town_id = fields.Many2one('l10n_cn.res.city.town', string='Town/Street', help='Town/Street are part of a city or district')
    country_code = fields.Char(related='country_id.code')

    @api.model
    def _fields_view_get_address(self, arch):
        if self.env.company.country_id.code == 'CN' or self.env.user.lang == 'zh_CN':
            doc = etree.fromstring(arch)
            if doc.xpath("//div[hasclass('o_address_cn')]"):
                return arch

            replacement_xml = """
                <div class="o_address_format o_address_cn">
                    <field name="type" invisible="1"/>
                    <field name="parent_id" invisible="1"/>
                    <field name="country_enforce_cities" invisible="1"/>
                    <field name="country_code" invisible="1"/>
                    <field name="country_id" class="o_address_country" placeholder="%(placeholder_country)s"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{'readonly': %(readonly_conditions)s}"
                    />
                    <field name="state_id" class="o_address_state" placeholder="%(placeholder_state)s"
                        domain="[('country_id', '=', country_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{
                            'invisible': [('country_code', 'in', ('HK', 'MO', 'TW'))],
                            'readonly': %(readonly_conditions)s
                        }"
                    />
                    <field name='city' class="o_address_city" placeholder="%(placeholder_city)s"
                        attrs="{
                            'invisible': [('country_enforce_cities', '=', True)],
                            'readonly': %(readonly_conditions)s
                        }"
                    />
                    <field name="city_id" class="o_address_city" placeholder="%(placeholder_city)s"
                        domain="['&amp;', ('country_id', '=', country_id), ('state_id', '=', state_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{
                            'invisible': [('country_enforce_cities', '=', False)],
                            'readonly': %(readonly_conditions)s
                        }"
                    />
                    <field name="l10n_cn_district_id" class="o_address_cn_district" placeholder="%(placeholder_district)s"
                        domain="[('city_id', '=', city_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{
                            'invisible': [('country_code', '!=', 'CN')],
                            'readonly': %(readonly_conditions)s}"
                    />
                    <field name="l10n_cn_town_id" class="o_address_cn_town" placeholder="%(placeholder_town)s"
                        domain="['&amp;', ('city_id', '=', city_id), ('district_id', '=', l10n_cn_district_id)]"
                        options='{"no_open": True, "no_create": True}'
                        attrs="{
                            'invisible': [('country_code', '!=', 'CN')],
                            'readonly': %(readonly_conditions)s
                        }"
                    />
                    <field name="street" class="o_address_street" placeholder="%(placeholder_street)s"
                        attrs="{'readonly': %(readonly_conditions)s}"
                    />
                    <field name="street2" class="o_address_street" placeholder="%(placeholder_street2)s"
                        attrs="{
                            'invisible': [('country_code', '=', 'CN')],
                            'readonly': %(readonly_conditions)s
                        }"
                    />
                    <field name="zip" class="o_address_zip" placeholder="%(placeholder_zip)s"
                        attrs="{'readonly': %(readonly_conditions)s}"
                    />
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
            for address_node in doc.xpath("//div[hasclass('o_address_format')]"):
                readonly_conditions = '[]'
                for node in address_node.iter('field'):
                    if node.get('attrs'):
                        eval_attrs = safe_eval(node.get('attrs'))
                        readonly_conditions = eval_attrs.get('readonly', [])
                        continue
                replacement_data['readonly_conditions'] = readonly_conditions
                replacement_formatted = replacement_xml % replacement_data
                replace_node = etree.fromstring(replacement_formatted)
                if address_node.get('name'):
                    replace_node.set('name', address_node.get('name'))
                address_node.getparent().replace(address_node, replace_node)

            # TDE CLEANME:
            for child_node in doc.xpath("//field[@name='child_ids']"):
                if child_node.get('context'):
                    context = child_node.get('context').replace("}", ", 'default_l10n_cn_town_id': l10n_cn_town_id, 'default_l10n_cn_district_id': l10n_cn_district_id, 'default_city_id': city_id}")
                    child_node.set('context', context)

            arch = etree.tostring(doc, encoding='unicode')
            self = self.with_context(no_address_format=True)
        return super(Partner, self)._fields_view_get_address(arch)

    @api.model
    def _address_fields(self):
        return super(Partner, self)._address_fields() + ['city_id', 'l10n_cn_district_id', 'l10n_cn_town_id']

    @api.model
    def _get_address_format(self):
        address_format = super(Partner, self)._get_address_format()
        if self.country_code == 'CN' and self.state_id.code in ('HK', 'MO', 'TW'):
            # 地址格式不显示省份名
            address_format = "%(country_name)s\n%(city)s %(district_name)s %(town_name)s\n%(street)s%(street2)s\n%(zip)s"
        return address_format

    def _display_address(self, without_company=False):
        """ Override of base _display_address method for china """
        if self.country_code == 'CN':
            address_format = self._get_address_format()
            args = {
                'state_code': self.state_id.code or '',
                'state_name': self.state_id.name or '',
                'country_code': self.country_id.code or '',
                'country_name': self._get_country_name(),
                'company_name': self.commercial_company_name or '',
                'district_name': self.l10n_cn_district_id.name or '',
                'town_name': self.l10n_cn_town_id.name or '',
            }
            for field in self._formatting_address_fields():
                args[field] = getattr(self, field) or ''
            if without_company:
                args['company_name'] = ''
            elif self.commercial_company_name:
                address_format = '%(company_name)s\n' + address_format
            return address_format % args
        return super(Partner, self)._display_address(without_company)

    def _display_address_depends(self):
        return super(Partner, self)._display_address_depends() + ['l10n_cn_district_id.name', 'l10n_cn_town_id.name']

    def _get_address_adcode(self):
        return self.country_code == 'CN' and (self.l10n_cn_town_id.adcode or self.l10n_cn_district_id.adcode) or self.city_id.adcode or self.state_id.adcode or ''

    def _get_address_area_code(self):
        return self.country_code == 'CN' and self.l10n_cn_district_id.area_code or self.city_id.area_code

    @api.model
    def _get_l10n_cn_state_codes_for_region(self):
        """ 港澳台如果安装本地化模块，省份转为国家/地区 """
        codes = []
        if self.env['ir.module.module'].search([('name', 'like', 'l10n_hk%'), ('state', '=', 'installed')]):
            codes.append('HK')
        if self.env['ir.module.module'].search([('name', 'like', 'l10n_mo%'), ('state', '=', 'installed')]):
            codes.append('MO')
        if self.env['ir.module.module'].search([('name', 'like', 'l10n_tw%'), ('state', '=', 'installed')]):
            codes.append('TW')
        return codes

    @api.onchange('country_id')
    def _onchange_country_id(self):
        """ Override """
        state_domain = []
        city_domain = ['&', ('country_id', '=', self.country_id.id), ('state_id', '=', self.state_id.id)]
        if self.country_id:
            state_domain = [('country_id', '=', self.country_id.id)]
            if self.country_id != self.state_id.country_id:
                self.state_id = False
            if self.country_id != self.city_id.country_id:
                self.city_id = False
        return {'domain': {'state_id': state_domain, 'city_id': city_domain}}

    @api.onchange('state_id')
    def _onchange_state(self):
        """ Override """
        city_domain = ['&', ('country_id', '=', self.country_id.id), ('state_id', '=', self.state_id.id)]
        if self.state_id:
            if self.state_id.country_id:
                self.country_id = self.state_id.country_id
            if self.country_code == 'CN':
                region_codes = self._get_l10n_cn_state_codes_for_region()
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
            if self.city_id.state_id != self.state_id:
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

    @api.model
    def _check_address_consistency(self, vals):
        if vals.get('state_id') and not vals.get('country_id'):
            state = self.env['res.country.state'].browse(vals['state_id'])
            vals['country_id'] = state.country_id.id
        if vals.get('city_id') or vals.get('city'):
            City = self.env['res.city']
            District = self.env['l10n_cn.res.city.district']
            Town = self.env['l10n_cn.res.city.town']
            city = City.browse(vals['city_id']) if vals.get('city_id') else City.search([('name', '=', vals['city'])])
            country_id = vals.get('country_id')
            state_id = vals.get('state_id')
            if state_id and city.state_id.id != state_id:
                city = City.search([('state_id', '=', state_id), '|', ('adcode', '=', city.adcode), ('name', '=', city.name)], limit=1)
            elif country_id and city.country_id.id != country_id:
                city = City.search([('country_id', '=', country_id), '|', ('adcode', '=', city.adcode), ('name', '=', city.name)], limit=1)
            else:
                vals['country_id'] = city.country_id.id
                vals['state_id'] = city.state_id.id
            vals['city_id'] = city.id
            vals['city'] = city.name
            vals['zip'] = city.zipcode

            district = District.browse(vals.get('l10n_cn_district_id'))
            if district and district.city_id != city:
                district = District.search([('city_id', '=', city.id), '|', ('adcode', '=', district.adcode), ('name', '=', district.name)], limit=1)
                vals['l10n_cn_district_id'] = district.id
                vals['zip'] = district.zipcode or city.zipcode

            if vals.get('l10n_cn_town_id'):
                town = Town.browse(vals['l10n_cn_town_id'])
                if town.city_id != city:
                    town = Town.search([('city_id', '=', city.id), '|', ('adcode', '=', town.adcode), ('name', '=', town.name)], limit=1)
                if town.district_id != district:
                    town = Town.search([('district_id', '=', district.id), '|', ('adcode', '=', town.adcode), ('name', '=', town.name)], limit=1)
                vals['l10n_cn_town_id'] = town.id

    def write(self, vals):
        address_fields = self._address_fields()
        if any(field in vals for field in address_fields):
            self._check_address_consistency(vals)
        return super(Partner, self).write(vals)

    @api.model
    def create(self, vals):
        if not self.env.context.get('import_file'):
            address_fields = self._address_fields()
            if any(field in vals for field in address_fields):
                self._check_address_consistency(vals)
        return super(Partner, self).create(vals)

    @api.model
    def _check_import_consistency(self, vals_list):
        super(Partner, self)._check_import_consistency(vals_list)
        for vals in vals_list:
            self._check_address_consistency(vals)

    def _get_country_name(self):
        country_name = super(Partner, self)._get_country_name()
        if self.country_code == 'CN' and self.state_id.code in ('HK', 'MO', 'TW'):
            country_name = self.state_id.name or country_name
        return country_name
