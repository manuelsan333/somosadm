# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Advance Auto Parts Search and Selection in Sale Order",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Sales",
    "license": "OPL-1",
    "summary": "Auto Parts Base Odoo, Auto Parts And Variants Management Manage Auto Parts & Variants Find High Quality Auto Parts Handle Auto Parts By Make Model Year Type Find Vehicle Details Module Odoo Equipment Maintenance Repair Operation Assets Maintenance Equipment Repair Maintenance Request Auto Parts Repair Auto Parts Maintenance Machine Maintenance Machine Repair Product Repair Assets Repair Car Repair Maintenance Product Maintenance",
    "description": """
If you have the number of products and selection of products at
the time of making a quotation it is a quite difficult task.
So don't worry we have a solution here we build a module that can
help to find a particular product from the product list.
In this module provide a button "Select Product Advance" in the sale order.
You can find auto parts in the product using a filter like a
type, make, model, year. Also, you can find the product using the
product attribute field. You can find a product by comparing price,
barcode, internal reference. sometimes some product is commonly required
so you can add product in 'specific' list and
you can add that product in the quotation.
This module saves your important time and reduces human error
as well as less effort.
Advance Auto Parts Search and Selection in Sale Order Odoo
Find Products From Sales Order Module, Filter Auto Parts From Quotations,
Search Auto Parts Based On Model ,Type, Make, Year Odoo,
Find Product By Comparing Price, Barcode, Internal Reference In So Odoo.
Find Products From So Module, Filter Auto Parts From Quotations App,
Search Auto Parts Based On Model, Find Auto Parts Based On Type,
Find Auto Parts Based On Make, Find Auto Parts Based On Year Odoo,
Find Product By Comparing Price, Find Product By Barcode,
Find Product By Internal Reference In Sales Order Odoo.
""",
    "version": "16.0.1",
    "depends": [
            # "web_domain_field",
            "sh_motorcycle_backend",
    ],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/sale_inherit_views.xml",
        "wizard/sh_smps_wizard_views.xml",
        "views/sh_settings_views.xml"],
    "images": ["static/description/background.png"],
    "live_test_url":
    "https://www.youtube.com/watch?v=8hZJlXeIsRQ&feature=youtu.be",
    "auto_install": False,
    "installable": True,
    "price": 80,
    "currency": "EUR"
}
