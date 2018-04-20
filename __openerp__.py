# -*- coding: utf-8 -*-
{
    'name': "gent",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mrp',
                'sale_layout',
                'sale',
                'product',
                'project'
    ],

    # always loaded
    'data': [
        'security/gent_security.xml',
        'security/ir.model.access.csv',
        'templates.xml',
        'views/avant_metre.xml',
        'views/bde.xml',
        'views/type_produit.xml',
        'views/coeff.xml',
        'views/ouvrage_elementaire.xml',
        'views/ouvrage_elementaire_data.xml',
        
        
        'views/facturation/facturation.xml',
        'datas/test.xlsx',
        'views/project/project.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
