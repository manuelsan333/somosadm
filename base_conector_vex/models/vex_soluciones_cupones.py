from odoo import api, fields, models
class Cupones(models.Model):
    _inherit = 'coupon.program'
    id_vex = fields.Char(string="Connector ID")
    conector = fields.Selection([])
    server_vex = fields.Many2one('vex.instance')
    _sql_constraints = [
        ('unique_id_cupones_vex', 'unique(id_vex, server_vex, conector)','There can be no duplication of synchronized Delivery')
    ]