# -*- coding: utf-8 -*-
import logging
import threading
from odoo import api, fields, models



_logger = logging.getLogger(__name__)


import requests
import base64

class Product(models.Model):
    _inherit               = 'product.template'
    id_vex                 = fields.Char(string="Connector  ID")
    server_vex = fields.Many2one('vex.instance')
    conector               = fields.Selection([])
    edit_id                = fields.Boolean(default=False)
    permalink              = fields.Char()
    img_url_vex            = fields.Char('Imagen Url')
    send_stock = fields.Boolean(string='Enviar Stock')
    warehouse_stock_vex = fields.Many2one('stock.warehouse',string="Almacen x Exportar")


    #_sql_constraints = [
    #    ('unique_id_prod_vex', 'unique(id_vex, conector, server_vex)',
    #     'There can be no duplication of synchronized Products Template')
    #]

    def export_conector_vex(self):
        return

    def update_conector_vex(self):
        return


    '''
    @api.onchange('img_url_vex')
    def change_image_vex(self):
        for record in self:
            image = None
            if record.img_url_vex:
                image = base64.b64encode(requests.get(record.img_url_vex.strip()).content).replace(b'\n', b'')
            record.write({'image_1920': image })
    '''


class Image(models.Model):
    _inherit        = 'product.image'
    id_vex          = fields.Char(string="Connector  ID")
    server_vex      = fields.Many2one('vex.instance')
    conector        = fields.Selection([])
    image_url_vex   = fields.Char(string="URL")
    dowloaded       = fields.Boolean(default=False)
    _sql_constraints = [
        ('unique_id_img_vex', 'unique(id_vex, conector, server_vex)',
         'There can be no duplication of synchronized Pictures ')
    ]

    def dowloand_write_img(self):
        for record in self:
            try:
                myfile = requests.get(record.image_url_vex)
            except:
                continue
            #except requests.ConnectionError:
            #    continue
            try:
                record.image_1920 = base64.b64encode(myfile.content)
                record.dowloaded = True
            except:
                continue

    def dowload_threading_images_website(self):
        th = []
        for record in self:
            if record.image_url_vex:
                threaded_synchronization = threading.Thread(
                    target=record.dowloand_write_img())
                th.append(threaded_synchronization)
            return
        for t in th:
            t.run()


    '''

    def dowload_threading_images_website(self):
        images = self.env['product.image'].search([('image_1920','=',False)])
        th = []
        for record in images:
            if record.image_url_vex:
                threaded_synchronization = threading.Thread(
                    target=record.dowloand_write_img())
                th.append(threaded_synchronization)
            return
        for t in th:
            t.run()
    '''
