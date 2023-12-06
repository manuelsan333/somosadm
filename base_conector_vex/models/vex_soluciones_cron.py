from odoo import api, fields, models
class Cron(models.Model):
    _inherit = 'ir.cron'
    '''
    argument   = fields.Char()
    automatic  = fields.Boolean(default=False)
    conector = fields.Selection([])
    server_vex = fields.Many2one('vex.instance')
    accion = fields.Many2one('vex.restapi.list')
    
    _sql_constraints = [
        ('unique_id_cron_conector', 'unique(argument,automatic,conector)', 'There can be no duplication of synchronized Argument')
    ]
    '''