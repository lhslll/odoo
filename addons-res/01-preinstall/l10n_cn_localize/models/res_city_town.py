# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class L10nCnResCityTown(models.Model):
    """ 县以下（镇、乡、街道）行政级别 """
    _name = 'l10n_cn.res.city.town'
    _description = 'Town/Street'
    _order = 'adcode, name'

    name = fields.Char(string='Name', required=True)
    adcode = fields.Char(string='Administrative Division Code', index=True, size=12)  # 行政区划代码
    # 目前部分城市和省直辖县因为没有区县的划分，在市级下方直接显示街道  Dong 2020-01-10
    city_id = fields.Many2one('res.city', string='City', required=True,
                              domain=lambda self: [('country_id', '=', self.env.ref('base.cn').id)])
    district_id = fields.Many2one('l10n_cn.res.city.district', string='District/County',
                                  domain="['&', ('city_id', '=', city_id), ('city_id', '!=', False)]")
    active = fields.Boolean('Active', default=True)

    @api.constrains('city_id', 'district_id', 'adcode', 'active')
    def _check_adcode(self):
        for town in self.filtered(lambda r: r.adcode):
            city_digits = self.env['res.city']._get_city_adcode_digits(town.adcode, town.city_id.country_id)
            matched_city_id = self.env['l10n_cn.res.city.district']._find_city_by_adcode(town.adcode, town.city_id.country_id)
            prefix_error = False
            if not town.adcode.isdigit() or len(town.adcode) < 6:
                raise ValidationError(_('The administrative division code of china must be a number'))
            elif matched_city_id and matched_city_id != town.city_id:
                raise ValidationError(_('The administrative division code (%s) belong to %s (%s)' % (town.adcode, matched_city_id.name, matched_city_id.adcode[0:city_digits])))
            elif town.city_id.adcode and town.adcode[0:city_digits] != town.city_id.adcode[0:city_digits]:
                prefix_error = True  # 校验市级前缀
            elif town.district_id and town.adcode[4:6] == '00':
                prefix_error = True  # 校验县级前缀
            elif town.district_id.adcode and town.adcode[0:6] != town.district_id.adcode[0:6]:
                prefix_error = True  # 校验县级前缀(非直辖县)

            elif len(town.adcode) > 6 and town.adcode[6:9] == '000':
                raise ValidationError(_('The administrative division code do not match coding rule'))

            if prefix_error:
                raise ValidationError(_('Incorrect administrative division code prefix'))

            domain = [('id', '!=', town.id), ('adcode', '=', town.adcode)]
            # 超过6位的区划代码不允许重复
            if town.active and len(town.adcode) > 6 and self.search(domain):
                raise ValidationError(_('The administrative division code of china must be unique'))
