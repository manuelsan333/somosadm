from odoo import api, fields, models
class Logs(models.Model):
    _name    = "vex.logs"
    vex_list    = fields.Many2one('vex.restapi.list')
    start_date  = fields.Datetime()
    end_date    = fields.Datetime()
    state       = fields.Selection([('error', 'Error'),('done', 'Done'),('unit','unit')])
    description = fields.Char()
    #server      = fields.Many2one('woo.synchro.server')
    page        = fields.Integer(string='Current Page')
    total       = fields.Integer(string='Total Page')
    stock       = fields.Boolean(default=False)
    webhook     = fields.Boolean(default=False)
    detail      = fields.Text()
    #conector = fields.Selection()
    server_vex = fields.Many2one('vex.instance')
    type = fields.Selection([('manual','Manual'),('automatic','Automatico')])