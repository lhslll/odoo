# -*- coding: utf-8 -*-
{
    'name': "bug管理",

    'summary': """
        bug的管理应用""",

    'description': """
        bug的管理应用
    """,

    'author': "LCZ",
    'website': "http://www.lczrockclimbing.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/bug.xml',
        'views/follower.xml',
        'views/templates.xml',
        'views/bug_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
