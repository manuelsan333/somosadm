from odoo import api, fields, models
class VexConfig(models.TransientModel):
    _name = 'vex.config'
    def get_conectores(self):
        conectores = [
            ('woo', 'WooCommerce'),
            ('meli', 'Mercado Libre'),
            ('shop', 'Shopify'),
            ('mag', 'Magento')
            ]
        return