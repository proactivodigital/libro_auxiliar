{
    'name': 'Libro auxiliar',
    'version': '1.0',
    'depends': ['base', 'account'],
    'author': 'Cristian Berrio',
    'category': 'Accounting',
    'description': 'Módulo para gestionar los medios magnéticos',
    'data': [
        'views/account_balance_sheet.xml',
        'data/security.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': "LGPL-3",
}
