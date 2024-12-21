{
    'name': 'Libro auxiliar',  # Name of the module in Odoo
    'version': '1.0',  # Version of the module
    'depends': ['base', 'account'],  # Module dependencies: 'base' and 'account' are essential Odoo modules
    'author': 'Cristian Berrio',  # Author of the module
    'category': 'Accounting',  # Module category in Odoo, in this case, it is Accounting
    'description': 'Módulo para gestionar los medios magnéticos',  # Short description of the module
    'data': [
        'views/account_balance_sheet.xml',  # View defining the design and content of balance sheets in the module
        'data/security.xml',  # Security configuration file that defines access permissions
    ],
    'installable': True,  # Indicates if the module is installable
    'application': False,  # Defines whether the module is a complete Odoo application or just a plugin
    'auto_install': False,  # Defines whether the module should be automatically installed when installing other modules
    'license': "LGPL-3",  # License under which the module is distributed
}
