{
    'name': 'Cuenta analitica con stock',
    'version': '0.1',
    'author': 'DGV',
    'website': 'https://github.com/AlfaSystemas5457/account_analytic_with_stock',
    'summary': 'Permite establecer relación entre los movimientos de stock y la cuentas analiticas.',
    'description':"""Permite establecer relación entre los movimientos de stock y la cuentas analiticas.""",
    'category': 'Accounting',
    'depends': ['stock_account', 'stock', 'purchase'],
    'data': [
        'views/account_views.xml',
        'views/add_lifo_view.xml'
        ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
