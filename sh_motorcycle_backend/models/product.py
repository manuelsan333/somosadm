# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    motorcycle_ids = fields.Many2many(
        'motorcycle.motorcycle',
        'product_product_motorcycle_motorcycle_rel',
        'product_id', 'motorcycle_id',
        string='Auto Parts', copy=True
    )
    sh_is_common_product = fields.Boolean(string = "Common Products?")
    @api.onchange('sh_is_common_product')
    def onchange_sh_is_common_product(self):
        if self:
            for record in self:
                if record.sh_is_common_product:
                    record.motorcycle_ids = False
