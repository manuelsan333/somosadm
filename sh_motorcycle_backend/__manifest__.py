# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Auto Parts Base",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "license": "OPL-1",
    "category": "Industries",
    "summary": "Auto Parts Base Odoo, Auto Parts And Variants Management Manage Auto Parts & Variants Find High Quality Auto Parts Handle Auto Parts By Make Model Year Type Find Vehicle Details Module Odoo Equipment Maintenance Repair Operation Assets Maintenance Equipment Repair Maintenance Request Auto Parts Repair Auto Parts Maintenance Machine Maintenance Machine Repair Product Repair Assets Repair Car Repair Maintenance Product Maintenance",
    "description": """
In automobile shops have numerous auto parts there is no count for
parts and it's variants that's the way it is quite difficult to
manage into the shop. So that's why we created a model that will
help you to manage it. This module will help to manage an
auto part by make, model, year, type. You can also assign vehicles
in auto parts product variants so it will become very easy to find
the product using vehicle details. In this module provide two groups
for user and manager so you can easily apply access rights
for user and manager. This is very clean and transparent
so the user can easily understand how it works.
Auto Parts Base Odoo, Auto Parts And Variants Management Odoo
Manage Auto Parts And Variants Module, Find High Quality Auto Parts,
Feature Of Maintain Auto Parts By Make, Model, Year, Type Odoo, Help
You For Search Right Vehicle Parts,
Assign Vehicles In Auto Parts Product Variants,
Find Product Using Vehicle Details For User And Manager Odoo.
Manage Auto Parts & Variants App, Find High Quality Auto Parts,
Handle Auto Parts By Make, Model, Year, Type,
Find Vehicle Details Module Odoo.
""",
    "version": "16.0.1",
    "depends": ["sale_management"],
    "data": [
            "security/sh_motorcycle_backend_groups.xml",
            "security/ir.model.access.csv",
            "views/sh_motorcycle_motorcycle_views.xml",
            "views/sh_motorcycle_type_views.xml",
            "views/sh_motorcycle_make_views.xml",
            "views/sh_motorcycle_mmodel_views.xml",
            "views/sh_motorcycle_year_views.xml",
            "views/product_views.xml",
            ],
    "images": ["static/description/background.png", ],
    "live_test_url":"https://www.youtube.com/watch?v=D-tXbNP38lM&feature=youtu.be",
    "application": True,
    "auto_install": False,
    "installable": True,
    "price": 80,
    "currency": "EUR",
}
