{
    'name': 'Cuenta analitica con stock',
    'version': '0.1',
    'author': 'DGV',
    # 'website': 'https://www.ganemo.co',
    'summary': 'Permite establecer relación entre los movimientos de stock y la cuentas analiticas.',
    'category': 'Accounting',
    'depends': ['stock_account', 'stock'],
    'data': ['views/account_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'Other proprietary'
}
