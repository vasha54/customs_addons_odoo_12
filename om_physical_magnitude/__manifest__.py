# -*- coding: utf-8 -*-
{
    'name': 'Physical Magnitude',
    'version': '12.0.0.0.3',
    'summary': 'Manager Physical Magnitude easily',
    'description': """
    The following module allows the management of physical magnitudes as well as the measurement units associated with each of the magnitudes. Among the 
 functionalities of the module are:\n
    \t\t -The creation, edition, visualization and elimination of physical magnitudes.\n
    \t\t -The creation, edition, visualization and deletion of measurement units.\n
    \t\t -The creation, edition, visualization and elimination of conversion of units that belong to the same physical quantity.\n\n
    To install this module it is necessary to have previously installed the python unidecode package.""",
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
        'views/views_unit_conversion.xml',
        'views/menu.xml'
        ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
 }