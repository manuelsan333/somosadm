from odoo import api, fields, models
class Inventory(models.Model):
    _inherit     = 'stock.inventory'
    stock_vex    = fields.Boolean(default=False)