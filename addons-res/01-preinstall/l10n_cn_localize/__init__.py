# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

from . import models


def _init_city_districts(cr, registry):
    from odoo.tools import convert_file
    convert_file(cr, 'l10n_cn_localize', 'data/l10n_cn.res.city.district.csv', None, mode='init', noupdate=True, kind='init', report=None)
    convert_file(cr, 'l10n_cn_localize', 'data/l10n_cn.res.city.town.csv', None, mode='init', noupdate=True, kind='init', report=None)
