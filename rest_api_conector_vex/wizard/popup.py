from odoo import api, fields, models
class VexPopup(models.TransientModel):
    _name = "vex.wizard.popup"
    msg = fields.Char()