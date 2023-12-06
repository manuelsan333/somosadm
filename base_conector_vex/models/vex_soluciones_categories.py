from odoo import api, fields, models



class Categories(models.Model):
    _inherit = 'product.public.category'
    id_vex = fields.Char(string="Id Connector")
    server_vex = fields.Many2one('vex.instance')

    conector = fields.Selection([])
    parent_id_vex_tmp = fields.Char()

