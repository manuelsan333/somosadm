from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    meli_shop_id = fields.Char()
    is_vex_line_shipment = fields.Boolean()



class Orders(models.Model):
    _inherit = 'sale.order'
    _description = "Ordenes de mercado libre"

    id_vex   = fields.Char(string="Connector ID",copy=False)
    conector = fields.Selection([],copy=False)
    server_vex = fields.Many2one('vex.instance',copy=False)
    shipping_vex = fields.Float(string="Shipping",copy=False)
    fee_vex = fields.Float(string="Fee",copy=False)
    primary_order_id = fields.Many2one('sale.order',string="Venta Primaria")
    secundary_order_ids = fields.One2many('sale.order','primary_order_id',string="Venta Secundaria")
    date_vex_order = fields.Datetime(string="Fecha Pedido")
    _sql_constraints = [
        ('unique_id_order_woo', 'unique(id_vex, server_vex , conector,primary_order_id)', 'There can be no duplication of synchronized Orders')
    ]

    def cancel_vex(self):
        return


