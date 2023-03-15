# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_search = fields.Boolean(string='Enable Search')
    enable_common_search = fields.Boolean(
        string='Display Common Product in Search')
    sh_hide_search_bar_for_mobile = fields.Boolean(string='Hide Search in Mobile')
    