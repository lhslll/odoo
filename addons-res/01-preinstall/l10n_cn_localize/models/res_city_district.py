# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class L10nCnResCityDistrict(models.Model):
    """ 县级市、区县行政级别 """
    _name = 'l10n_cn.res.city.district'
    _description = 'District/County'
    _order = 'adcode, name'

    name = fields.Char(string='Name', required=True, translate=True)
    adcode = fields.Char(string='Administrative Division Code', index=True, size=6)  # 行政区划代码
    # 部分城市的区县存在区号不一致
    area_code = fields.Char(string='Area Code')  # 区号
    zipcode = fields.Char("Zip")  # 区县邮编
    state_id = fields.Many2one('res.country.state', string='Province', required=True,
                               domain=lambda self: [('country_id', '=', self.env.ref('base.cn').id)])
    city_id = fields.Many2one('res.city', string='City',
                              domain="['&', ('state_id', '=', state_id), ('state_id', '!=', False)]")
    active = fields.Boolean('Active', default=True)

    @api.constrains('city_id', 'adcode', 'active')
    def _check_adcode(self):
        for district in self.filtered(lambda r: r.adcode):
            city_digits = self.env['res.city']._get_city_adcode_digits(district.adcode, district.state_id.country_id)
            matched_city_id = self._find_city_by_adcode(district.adcode, district.state_id.country_id)
            prefix_error = False
            if not district.adcode.isdigit() or len(district.adcode) != 6:
                raise ValidationError(_('The administrative division code of china must be a six-digit number'))
            elif district.city_id and matched_city_id and matched_city_id != district.city_id:
                raise ValidationError(_('The administrative division code (%s) belong to %s (%s)' % (district.adcode, matched_city_id.name, matched_city_id.adcode[0:city_digits])))
            elif district.state_id.adcode and district.adcode[0:2] != district.state_id.adcode[0:2] or district.adcode[0] in ('0', '9'):
                prefix_error = True  # 校验省级前缀
            elif district.adcode[0] not in ('7', '8') and district.adcode[2:4] == '00':
                prefix_error = True  # 校验市级前缀
            elif district.city_id.adcode and district.adcode[0:city_digits] != district.city_id.adcode[0:city_digits]:
                prefix_error = True  # 校验市级前缀

            elif district.adcode[4:6] == '00':
                raise ValidationError(_('The administrative division code do not match coding rule'))

            if prefix_error:
                raise ValidationError(_('Incorrect administrative division code prefix'))

            domain = [('id', '!=', district.id), ('adcode', '=', district.adcode)]
            if district.active and self.search(domain):
                raise ValidationError(_('The administrative division code of china must be unique'))

    @api.model
    def _find_city_by_adcode(self, adcode, country_id):
        City = self.env['res.city']
        if country_id and country_id.code == 'CN':
            city_digits = City._get_city_adcode_digits(adcode, country_id)
            suffix = ''
            if city_digits == 4:
                suffix = '00'
            elif city_digits == 2:
                # 直辖市下辖的县级行政区当前简化后统一汇总到市辖区('0200','0300'合并到'0100')
                suffix = '0100'
            adcode = adcode[0:city_digits] + suffix
        return City.search([('adcode', '=', adcode), ('country_id', '=', country_id.id)], limit=1)

    @api.model
    def create(self, vals):
        if vals.get('adcode') and not vals.get('city_id'):
            state_id = self.env['res.country.state'].browse(vals.get('state_id'))
            matched_city_id = self._find_city_by_adcode(vals['adcode'], state_id.country_id)
            if matched_city_id:
                vals['city_id'] = matched_city_id.id
        if vals.get('city_id') and not vals.get('area_code'):
            city_id = self.env['res.city'].browse(vals['city_id'])
            vals['area_code'] = city_id.area_code
        return super(L10nCnResCityDistrict, self).create(vals)

    def write(self, vals):
        if vals.get('adcode') and 'city_id' not in vals and not self.city_id:
            state_id = self.env['res.country.state'].browse(vals.get('state_id')) or self.state_id
            matched_city_id = self._find_city_by_adcode(vals['adcode'], state_id.country_id)
            if matched_city_id:
                vals['city_id'] = matched_city_id.id
        return super(L10nCnResCityDistrict, self).write(vals)
