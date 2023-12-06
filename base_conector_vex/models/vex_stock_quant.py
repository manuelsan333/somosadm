from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def write(self,values):
        res = super().write(values)

        if len(self) == 1:
            if self.product_id:
                self.product_id.update_conector_vex()
        return res