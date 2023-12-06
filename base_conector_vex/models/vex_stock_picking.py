from odoo import api, fields, models
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def export_vex_product(self):
        export_stock = False
        instances = self.env['vex.instance'].search([])
        if instances:
            for instance in instances:
                if instance.update_stock:
                    export_stock = True
        if export_stock:
            products = []
            for line in self.move_line_ids_without_package:
                if line.product_id and line.product_id.id_vex_varition:
                    if line.product_id.id not in products:
                        products.append(line.product_id.id)

            if products:
                productss = self.env['product.product'].search([('id', 'in', products)])
                productss.update_conector_vex()


    def button_validate(self):
        res = super().button_validate()
        self.export_vex_product()
        return res