# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class City(models.Model):
    _inherit = 'res.city'
    _order = 'adcode, name'

    adcode = fields.Char(string='Administrative Division Code', index=True)  # 行政区划代码
    area_code = fields.Char(string='Area Code')  # 区号
    active = fields.Boolean('Active', default=True)

    @api.constrains('country_id', 'state_id', 'adcode', 'active')
    def _check_adcode(self):
        for city in self.filtered(lambda r: r.adcode and r.country_id.code == 'CN'):
            matched_state_id = self._find_state_by_adcode(city.adcode, city.country_id)
            if not city.adcode.isdigit() or len(city.adcode) != 6:
                raise ValidationError(_('The administrative division code of china must be a six-digit number'))
            elif city.state_id and matched_state_id and city.state_id != matched_state_id:
                raise ValidationError(_('The administrative division code (%s) belong to %s (%s)' % (city.adcode, matched_state_id.name, matched_state_id.adcode[0:2])))
            elif city.state_id.adcode and city.adcode[0:2] != city.state_id.adcode[0:2] or city.adcode[0] in ('0', '9'):
                raise ValidationError(_('Incorrect administrative division code prefix'))
            elif city.adcode[2:4] == '00' or city.adcode[2] == '8' or city.adcode[2] == '9' and (city.adcode[3] != '0' or city.adcode[4:6] == '00'):
                raise ValidationError(_('The administrative division code do not match coding rule'))
            elif city.adcode[2] != '9' and city.adcode[4:6] != '00':
                raise ValidationError(_('Incorrect administrative division code suffix'))
            domain = [('id', '!=', city.id), ('country_id', '=', city.country_id.id), ('adcode', '=', city.adcode)]
            if city.active and self.search(domain):
                raise ValidationError(_('The administrative division code of china must be unique'))

    @api.model
    def default_get(self, fields):
        result = super(City, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        if active_model in ('l10n_cn.res.city.district', 'l10n_cn.res.city.town'):
            result['country_id'] = self.env.ref('base.cn').id
        return result

    @api.model
    def _get_city_adcode_digits(self, adcode, country_id):
        """ 城市类型判断 """
        digits = 0
        if country_id and country_id.code == 'CN':
            digits = 4  # 地级市，验证前4位
            if adcode[0:2] in ('11', '12', '31', '50') :
                digits = 2  # 直辖市，验证前2位
            if adcode[2:4] == '90' and adcode[4:6] != '00':
                digits = 6  # 直辖县，验证前6位
        return digits

    @api.model
    def _find_state_by_adcode(self, adcode, country_id):
        if country_id and country_id.code == 'CN':
            adcode = adcode[0:2].ljust(6, '0')
        return self.env['res.country.state'].search([('adcode', '=', adcode), ('country_id', '=', country_id.id)], limit=1)

    @api.model
    def create(self, vals):
        if vals.get('adcode') and not vals.get('state_id'):
            country_id = self.env['res.country'].browse(vals.get('country_id'))
            matched_state_id = self._find_state_by_adcode(vals['adcode'], country_id)
            if matched_state_id:
                vals['state_id'] = matched_state_id.id
        return super(City, self).create(vals)

    def write(self, vals):
        if vals.get('adcode') and 'state_id' not in vals and not self.state_id:
            country_id = self.env['res.country'].browse(vals.get('country_id')) or self.country_id
            matched_state_id = self._find_state_by_adcode(vals['adcode'], country_id)
            if matched_state_id:
                vals['state_id'] = matched_state_id.id
        return super(City, self).write(vals)
