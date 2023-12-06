from odoo import api, fields, models
class Envios(models.Model):
    _inherit = 'delivery.carrier'
    id_vex = fields.Char(string="Connector ID")
    conector = fields.Selection([])
    server_vex = fields.Many2one('vex.instance')
    _sql_constraints = [
        ('unique_id_envios_vex', 'unique(id_vex, server_vex,conector)',
         'There can be no duplication of synchronized Delivery')
    ]