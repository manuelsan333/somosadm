from odoo import api, fields, models


class Customers(models.Model):
    _name           = 'res.partner'
    _inherit        = 'res.partner'
    id_vex          = fields.Char(string="Meli ID")
    #id_customer     = fields.Char(string="Customer ID")
    id_vex_parent  = fields.Char(string="Meli ID Parent")
    #nickname        = fields.Char(string="Customer Nickname")
    conector = fields.Selection([])
    server_vex = fields.Many2one('vex.instance')
    _sql_constraints = [
        ('unique_id_clie_vex', 'unique(id_vex, conector)',
         'There can be no duplication of synchronized clients')
    ]
