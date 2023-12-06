from odoo import api, fields, models

class ProductProductExport(models.Model):
    _name           = 'vex.product.product.conector'
    product_id      = fields.Many2one('product.product')
    instance        = fields.Many2one('vex.instance')
    id_vex_varition = fields.Char(string="ID Variation")
    id_vex          = fields.Char(string="ID")
    _sql_constraints = [
        ('unique_product_conector', 'unique(instance , id_vex, id_vex_varition)',
         'There can be no duplication of synchronized Orders')
    ]

    def export_vex(self):
        return
