# -*- coding: utf-8 -*-
{
    'name': "bug管理advanced",

    'summary': """
        bug的管理应用advanced""",

    'description': """
        bug的管理应用advanced
    """,

    'author': "LCZ",
    'website': "http://www.lczrockclimbing.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['bug-management','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/bug_adv.xml',
        'views/bug_stage.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
