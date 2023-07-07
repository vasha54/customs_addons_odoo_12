# -*- coding: utf-8 -*-
{
    'name': 'My Library',
    'summary': "Manage books easily",
    'description': """Long description""",
    'author': "Luis Andrés Valido Fajardo",
    'website': "http://www.example.com",
    'category': 'Uncategorized',
    'version': '12.0.1',
    'depends': ['base','decimal_precision'],
    'data': [
             'security/groups.xml',
             'security/ir.model.access.csv',
             'views/library_book.xml',
             'views/menu.xml'
            ],
    'demo': [],
}