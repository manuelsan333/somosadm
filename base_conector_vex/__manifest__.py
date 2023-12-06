# -*- coding: utf-8 -*-
{
    'name': "Multi Base Vex Connector",
    'summary': """
      Base Vex Connector """,

    'description': """
        Base Vex Connector
    """,
    'author': "Vex Soluciones",
    'website': "https://www.pasarelasdepagos.com/",

    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    #'depends': ['rest_api_conector_vex','base','stock','contacts','sale_management','delivery'],
    'depends': ['rest_api_conector_vex','base','stock', 'website_sale','contacts','sale_management','delivery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/group.xml',
        'views/vex_product_template.xml',
        'views/vex_product_product.xml',
        'views/mensajes.xml',
        'views/customer.xml',
        'views/vex_instance.xml',
        'views/vex_order.xml',
        'views/vex_list.xml',
        'views/vex_logs.xml',
        'views/atributos.xml',
        'wizard/vex_synchro.xml',
        'data/vex_cron.xml',
        'data/product.xml',
        'views/product_image.xml',
        'views/vex_soluciones_categories.xml'
    ],

    #'images': ['static/description/odoo-woo.gif'],
}