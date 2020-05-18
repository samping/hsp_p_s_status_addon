# Copyright 2020  HSP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "销售采购状态增强 by HSP",

    'summary': """销售采购状态增强 by HSP
    """,
   'license': 'LGPL-3',
   'description': """
    销售采购状态增强 by HSP
   """,
    'author': 'HSP',
    'website': "https://www.garage-kit.com",
    'images': ['static/description/logo.png'],
    'category': 'Tools',
    'version': '13.0.1.0.0',
  
    'depends': [
        'purchase', 'sale',
    ],
    'data': [
        'views/purchase.xml',
        'views/sale.xml'
    ],
    # 'demo': [
    #     'demo/report.xml',
    # ],
    'installable': True,
}
