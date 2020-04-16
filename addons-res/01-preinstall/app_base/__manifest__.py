# -*- coding: utf-8 -*-

# Created on 2019-09-02
# author: 广州尚鹏，https://www.sunpop.cn
# email: 300883@qq.com
# resource of Sunpop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# Odoo12在线用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/12.0/zh_CN/index.html

# Odoo12在线开发者手册（长期更新）
# https://www.sunpop.cn/documentation/12.0/index.html

# Odoo10在线中文用户手册（长期更新）
# https://www.sunpop.cn/documentation/user/10.0/zh_CN/index.html

# Odoo10离线中文用户手册下载
# https://www.sunpop.cn/odoo10_user_manual_document_offline/
# Odoo10离线开发手册下载-含python教程，jquery参考，Jinja2模板，PostgresSQL参考（odoo开发必备）
# https://www.sunpop.cn/odoo10_developer_document_offline/

##############################################################################
#    Copyright (C) 2009-TODAY Sunpop.cn Ltd. https://www.sunpop.cn
#    Author: Ivan Deng，300883@qq.com
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#    See <http://www.gnu.org/licenses/>.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

{
    'name': "Separate Customer Vendor / Supplier in Sale and Purchase",
    'version': '13.20.02.01',
    'author': 'Sunpop.cn',
    'category': 'Base',
    'website': 'https://www.sunpop.cn',
    'license': 'LGPL-3',
    'sequence': 2,
    'price': 0.00,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'depends': [
        'partner_autocomplete',
        'sale',
        'purchase',
    ],
    'summary': """
    Show only customer in sale, Show only vendor in purchase.
    Quick set and view and search customer, vendor supplier for partner. 
    Done for related apps like Account, Crm.
    """,
    'description': """    
    Support Odoo 13， Enterprise and Community Edition
    1. Add customer, vendor field to partner. Quick set / view / search.
    2. Show only customer in sale order. sale only customer. Customer Priority. This can be configure.(odoo 13 only)
    3. Show only vendor in purchase order. purchase only supplier. Supplier Priority. This can be configure.(odoo 13 only)
    4. Done for related apps like Account, CRM
    5. Multi-language Support.
    6. Multi-Company Support.
    7. Support Odoo 13，12, Enterprise and Community Edition
    ==========
    1. 往来单位增加是否客户，是否供应商字段的处理
    2. 销售只显示客户，此项可配置 (仅odoo 13)
    3. 采购只显示供应商，此项可配置 (仅odoo 13)
    4. 适用各销售采购相关模块，如财务，CRM等
    5. 多语言支持
    6. 多公司支持
    7. Odoo 13,12, 企业版，社区版，多版本支持
    """,
    'data': [
        # 'security/*.xml',
        'security/res_group.xml',
        # 'data/.xml',
        'views/res_partner_views.xml',
        'views/sale_config_settings_views.xml',
        'views/purchase_config_settings_views.xml',
        # 用py 处理，不用 js 处理
        # 'views/templates.xml',
        # 'report/.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'js': [],
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
}
