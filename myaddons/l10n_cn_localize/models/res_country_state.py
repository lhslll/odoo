# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResCountryState(models.Model):
    _inherit = 'res.country.state'
    _order = 'adcode, code'

    name = fields.Char(translate=True)  # without l10n_multilang module
    adcode = fields.Char(string='Administrative Division Code', index=True)  # 行政区划代码

    @api.constrains('country_id', 'adcode')
    def _check_adcode(self):
        for state in self.filtered(lambda r: r.adcode and r.country_id.code == 'CN'):
            if not state.adcode.isdigit() or len(state.adcode) != 6:
                raise ValidationError(_('The administrative division code of china must be a six-digit number'))
            elif state.adcode[0] in ('0', '9'):
                raise ValidationError(_('The administrative division code do not match coding rule'))
            elif state.adcode[2:6] != '0000':
                raise ValidationError(_('Incorrect administrative division code suffix'))
            domain = [('id', '!=', state.id), ('country_id', '=', state.country_id.id), ('adcode', '=', state.adcode)]
            if self.search(domain):
                raise ValidationError(_('The administrative division code of china must be unique'))

    @api.model
    def default_get(self, fields):
        result = super(ResCountryState, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        if active_model in ('l10n_cn.res.city.district', 'l10n_cn.res.city.town'):
            result['country_id'] = self.env.ref('base.cn').id
        return result

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            lang = self.env.user.lang or ''
            if not (record.country_id.code in lang):
                name = "{} ({})".format(record.name, record.country_id.code)
            result.append((record.id, name))
        return result
