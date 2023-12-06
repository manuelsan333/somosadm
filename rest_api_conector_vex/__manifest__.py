# -*- encoding: utf-8 -*-
{
    'name': 'Odoo  Api Rest Connector',
    'summary': """
       Enables a REST API for the Odoo server.  With the API can generated  token authenticate . 
       Afterwards, a set of routes to interact with the server are provided. 
       The API can be used by any language or framework which can make an 
       HTTP requests and receive responses with JSON payloads and works with both 
       the Community and the Enterprise Edition. 
       """,

    'description': """
       Enables a REST API for the Odoo server.  With the API can generated  token authenticate . 
       Afterwards, a set of routes to interact with the server are provided. 
       The API can be used by any language or framework which can make an 
       HTTP requests and receive responses with JSON payloads and works with both 
       the Community and the Enterprise Edition. 
    """,

    'category': 'vex',
    'author': "Vex Soluciones",
    'website': "https://www.vexsoluciones.com",
    'depends': ['base'],
    'version': '1.0',
    'price': 50.00,
    'currency': 'USD',
    'auto_install': False,
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/webservice.xml',
        'wizard/wizard.xml'
        ],
    'installable': True,
    'images': ['static/description/portada.png'],
}