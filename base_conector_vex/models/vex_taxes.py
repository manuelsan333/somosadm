from odoo import api, fields, models
class Impuestos(models.Model):
    _inherit = 'account.tax'
    id_vex = fields.Char(string="Connector ID")
    conector = fields.Selection([])
    server_vex = fields.Many2one('vex.instance')
    _sql_constraints = [
        ('unique_id_impuestos_vex', 'unique(id_vex, server_vex, conector)',
         'There can be no duplication of synchronized Taxes')
    ]