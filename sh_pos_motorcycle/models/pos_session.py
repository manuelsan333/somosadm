# Copyright (C) Softhealer Technologies.
# Part of Softhealer Technologies.

from odoo import models, fields, api

class PosSessionInherit(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        if result:
            if result.get('search_params') and result.get('search_params').get('fields'):
                result.get('search_params').get('fields').append('sh_is_common_product')
                result.get('search_params').get('fields').append('motorcycle_ids')
        return result

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()

        if 'motorcycle.type' not in result:
            result.append('motorcycle.type')
        
        if 'motorcycle.make' not in result:
            result.append('motorcycle.make')

        if 'motorcycle.mmodel' not in result:
            result.append('motorcycle.mmodel')
        
        if 'motorcycle.motorcycle' not in result:
            result.append('motorcycle.motorcycle')

        if 'motorcycle.year' not in result:
            result.append('motorcycle.year')
       
        return result

    def _loader_params_motorcycle_type(self):
        return {'search_params': {'domain': [], 'fields': [], 'load': False}}

    def _get_pos_ui_motorcycle_type(self, params):
        return self.env['motorcycle.type'].search_read(**params['search_params'])

    def _loader_params_motorcycle_make(self):
        return {'search_params': {'domain': [], 'fields': [], 'load': False}}

    def _get_pos_ui_motorcycle_make(self, params):
        return self.env['motorcycle.make'].search_read(**params['search_params'])
    
    def _loader_params_motorcycle_mmodel(self):
        return {'search_params': {'domain': [], 'fields': [], 'load': False}}

    def _get_pos_ui_motorcycle_mmodel(self, params):
        return self.env['motorcycle.mmodel'].search_read(**params['search_params'])

    def _loader_params_motorcycle_motorcycle(self):
        return {'search_params': {'domain': [], 'fields': [], 'load': False}}

    def _get_pos_ui_motorcycle_motorcycle(self, params):
        return self.env['motorcycle.motorcycle'].search_read(**params['search_params'])

    def _loader_params_motorcycle_year(self):
        return {'search_params': {'domain': [], 'fields': [], 'load': False}}

    def _get_pos_ui_motorcycle_year(self, params):
        return self.env['motorcycle.year'].search_read(**params['search_params'])
