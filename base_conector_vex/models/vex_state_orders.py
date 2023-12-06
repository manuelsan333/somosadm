from odoo import api, fields, models

class OrderStatus(models.Model):
    _name = "vex.status.orders"
    name = fields.Char(required=True)
    value = fields.Char(required=True)

    conector = fields.Char(required=True)
    _sql_constraints = [
        ('unique_value', 'unique(value,conector)', 'There can be no duplication of synchronized status')
    ]
class InstanceOrderStatus(models.Model):
    _name = "vex.instance.status.orders"
    instance = fields.Many2one('vex.instance', required=True)
    conector = fields.Selection(related="instance.conector")
    #conector_char = fields.Char(compute="get_conec")
    state   = fields.Many2one('vex.status.orders')
    value = fields.Char(related='state.value')
    odoo_state = fields.Selection([('draft', 'Quotation'), ('send', 'Quotation Send'),
                                   ('sale', 'Sales Order'), ('done', 'Locked'),
                                   ('cancel', 'Cancelled')], required=True, default='draft')


    created_invoice = fields.Boolean(default=False)
    confirm_invoice = fields.Boolean(default=False, string="Confirmar Factura")
    created_shipment = fields.Boolean(default=False)
    confirm_albaran = fields.Boolean(default=False,string="Confirmar Albaran")

    _sql_constraints = [
        ('unique_value', 'unique(state,instance)', 'There can be no duplication of synchronized status')
    ]



    '''
    def get_conec(self):
        for record in self:
            record.
    '''
