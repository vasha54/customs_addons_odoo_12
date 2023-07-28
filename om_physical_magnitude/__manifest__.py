# -*- coding: utf-8 -*-
{
    'name': 'Physical Magnitude',
    'version': '12.0.0.0.2',
    'summary': 'Manager Physical Magnitude easily',
    'description': """Module for managing physical magnitudes as well as the units of measurement associated with them.""",
    'category': 'Tools',
    'author': 'Luis Andrés Valido Fajardo',
    'maintainer': 'Luis Andrés Valido Fajardo',
    'company': 'Luis Andrés Valido Fajardo',
    'website': 'https://github.com/vasha54/customs_addons_odoo_12',	
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/search_filters.xml',
        'views/views_magnitude.xml',
        'views/views_unit_measurement.xml',
        'views/view_unit_conversion.xml',
        'views/menu.xml'
        ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
 }