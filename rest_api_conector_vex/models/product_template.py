# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models
from odoo.addons.payment.models.payment_acquirer import ValidationError


_logger = logging.getLogger(__name__)


import requests
import base64

class Product(models.Model):
    _inherit               = 'product.template'

    permalink              = fields.Char()
