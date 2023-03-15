# Copyright (C) Softhealer Technologies.
from odoo import fields, models

class ResConfigSettingInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_enable_search = fields.Boolean(related="pos_config_id.enable_search", string='Enable Search', readonly=False)
    pos_enable_common_search = fields.Boolean(related="pos_config_id.enable_common_search",
        string='Display Common Product in Search',readonly=False)
    pos_sh_hide_search_bar_for_mobile = fields.Boolean(related="pos_config_id.sh_hide_search_bar_for_mobile",string='Hide Search in Mobile',readonly=False)
