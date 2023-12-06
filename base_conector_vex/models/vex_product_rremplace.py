from odoo import api, fields, models

class InstanceOrderStatus(models.Model):
    _name = "vex.instance.product.reemplace"
    instance = fields.Many2one('vex.instance', required=True)
    conector = fields.Selection(related="instance.conector")
    code  = fields.Char(string="Sku / ID",required=True)
    product_id = fields.Many2one('product.product',Required=True)
