# -*- coding: utf-8 -*-
# Copyright(c): 2019 Freshoo (<www.freshoo.cn>)

{
    'name': "China - Localization",
    'version': '13.0.1.1.2',
    'license': 'AGPL-3',
    'summary': """Chinese Localization""",
    'description': """
Includes the following localization data
================================================================

Province data with administrative division code / 包含行政区划代码的省份数据

City data with administrative division code / 包含行政区划代码的城市数据

District data with administrative division code / 包含行政区划代码的区县数据

Town/Street data with administrative division code / 包含行政区划代码的乡镇、街道数据

Main Features
-------------
* Province, city and district three-level linkage / 省市区三级联动
* Add address extension below city level / 增加市级以下的地址扩展
* Administrative divisions code rules check / 行政区划代码编码规则校验
* Address consistency check / 地址一致性校验

This module will take time to create town with 43k data / 加载43000条乡镇数据，请耐心等候
""",
    'author': 'dong@freshoo.cn',
    'website': 'https://www.freshoo.cn',
    'images': ['static/description/banner.png'],
    'category': 'Localization',
    'depends': ['base_setup','base_address_city'],
    'excludes': ['l10n_cn_city'],
    'data': [
        'security/localize_security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/res_country_state_views.xml',
        'views/res_city_views.xml',
        'views/res_city_district_views.xml',
        'views/res_city_town_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/res_config_settings_views.xml',
        'data/res_country_data.xml',
        'data/res_country_state_data.xml',
        'data/res_city_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': '_init_city_districts',
}
