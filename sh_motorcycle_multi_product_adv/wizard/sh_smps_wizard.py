# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import json

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MotorcycleAdvWizard(models.TransientModel):
    _name = "motorcycle.adv.wizard"
    _description = "Motorcycle Multi Product Selection Advanced Wizard"

    product_ids = fields.One2many(
        "motorcycle.adv.wizard.product.line", "motorcycle_adv_wizard_id", string="Products")
    product_attr_ids = fields.Many2many(
        "product.attribute.value", string="Attributes", ondelete="cascade")
    specific_product_ids = fields.One2many(
        "motorcycle.adv.wizard.product.line.specific", "motorcycle_adv_wizard_id_specific", string="Specific Products")

    type_id = fields.Many2one(comodel_name="motorcycle.type", string="Type")

    make_id_domain = fields.Char(string="Make Domain")
    mmodel_id_domain = fields.Char(string="Model Domain")
    year_id_domain = fields.Char(string="year Domain")

    make_id = fields.Many2one(comodel_name="motorcycle.make", string="Make",)
    mmodel_id = fields.Many2one(
        comodel_name="motorcycle.mmodel", string="Model")
    year_id = fields.Many2one(comodel_name="motorcycle.year", string="Year")

    action = {'name': 'Select Products Advance', 'view_mode': 'form', 'res_model': 'motorcycle.adv.wizard',
              'view_id': False, 'type': 'ir.actions.act_window', 'target': 'new'}

    def _default_domain(self):
        self.make_id_domain = json.dumps([('id', '!=', False)])
        self.mmodel_id_domain = json.dumps([('id', '!=', False)])
        self.year_id_domain = json.dumps([('id', '!=', False)])

    @ api.onchange('type_id')
    def _onchage_type_id(self):
        domain_dic = {}
        self.mmodel_id = False
        self.year_id = False
        self.make_id = False

        if self.type_id:
            mmodel_obj = self.env['motorcycle.mmodel']
            domain = [('type_id', '=', self.type_id.id)]
            mmodels = mmodel_obj.search(domain)
            if mmodels:
                make_ids = []
                for model in mmodels:
                    if model.make_id:
                        make_ids.append(model.make_id.id)

                domain_dic.update({'make_id': [('id', 'in', make_ids)], 'mmodel_id': [
                                  ('id', 'in', mmodels.ids)]})
            else:
                domain_dic.update(
                    {'make_id': [('id', 'in', [])], 'mmodel_id': [('id', 'in', [])]})
            search_m = self.env['motorcycle.motorcycle'].sudo().search(domain)
            if search_m:
                year_ids = []
                for motorcycle in search_m:
                    if motorcycle.year_id:
                        year_ids.append(motorcycle.year_id.id)
                domain_dic.update({'year_id': [('id', 'in', year_ids)]})
            else:
                domain_dic.update({'year_id': [('id', 'in', [])]})
        else:
            domain_dic.update({'make_id': [('id', '!=', False)], 'mmodel_id': [
                              ('id', '!=', False)], 'year_id': [('id', '!=', False)]})

        self.make_id_domain = json.dumps(domain_dic.get('make_id'))
        self.mmodel_id_domain = json.dumps(domain_dic.get('mmodel_id'))
        self.year_id_domain = json.dumps(domain_dic.get('year_id'))

    @ api.onchange('make_id')
    def _onchage_make_id(self):
        domain_dic = {}
        self.mmodel_id = False
        self.year_id = False
        if self.make_id:
            mmodel_obj = self.env['motorcycle.mmodel']
            domain = [('make_id', '=', self.make_id.id)]
            if self.type_id:
                domain.append(('type_id', '=', self.type_id.id))

            mmodels = mmodel_obj.search(domain)
            if mmodels:
                domain_dic.update({'mmodel_id': [('id', 'in', mmodels.ids)]})
            else:
                domain_dic.update({'mmodel_id': [('id', 'in', [])]})
            search_m = self.env['motorcycle.motorcycle'].sudo().search(domain)
            if search_m:
                year_ids = []
                for motorcycle in search_m:
                    if motorcycle.year_id:
                        year_ids.append(motorcycle.year_id.id)
                domain_dic.update({'year_id': [('id', 'in', year_ids)]})
            else:
                domain_dic.update({'year_id': [('id', 'in', [])]})
        else:
            domain_dic.update(
                {'mmodel_id': [('id', '!=', False)], 'year_id': [('id', '!=', False)]})

        self.mmodel_id_domain = json.dumps(domain_dic.get('mmodel_id'))
        self.year_id_domain = json.dumps(domain_dic.get('year_id'))

    @ api.onchange('mmodel_id')
    def _onchage_mmodel_id(self):
        domain_dic = {}
        self.year_id = False
        if self.mmodel_id:
            domain = [('mmodel_id', '=', self.mmodel_id.id)]
            if self.make_id:
                domain.append(('make_id', '=', self.make_id.id))
            search_m = self.env['motorcycle.motorcycle'].sudo().search(domain)
            if search_m:
                year_ids = []
                for motorcycle in search_m:
                    if motorcycle.year_id:
                        year_ids.append(motorcycle.year_id.id)
                domain_dic.update({'year_id': [('id', 'in', year_ids)]})
            else:
                domain_dic.update({'year_id': [('id', 'in', [])]})
        else:
            domain_dic.update({'year_id': [('id', '!=', False)]})

        self.year_id_domain = json.dumps(domain_dic.get('year_id'))

    @ api.onchange('year_id')
    def _onchage_year_id(self):
        domain_dic = {}
        if self.year_id:
            domain = [('year_id', '=', self.year_id.id)]
            if self.make_id:
                domain.append(('make_id', '=', self.make_id.id))
            if self.mmodel_id:
                domain.append(('mmodel_id', '=', self.mmodel_id.id))
            if self.type_id:
                domain.append(('type_id', '=', self.type_id.id))

            search_m = self.env['motorcycle.motorcycle'].sudo().search(domain)
            if search_m:
                mmodel_ids = []
                for motorcycle in search_m:
                    if motorcycle.year_id:
                        mmodel_ids.append(motorcycle.mmodel_id.id)
                domain_dic.update({'mmodel_id': [('id', 'in', mmodel_ids)]})
            else:
                domain_dic.update({'mmodel_id': [('id', 'in', [])]})
        else:
            domain_dic.update({'mmodel_id': [('id', '!=', False)]})

        self.mmodel_id_domain = json.dumps(domain_dic.get('mmodel_id'))

    def sh_motorcycle_adv_select_product(self, product_ids):

        if self and product_ids and self.env.context.get('sh_motorcycle_adv_so_id', False):
            order_id = self.env.context.get('sh_motorcycle_adv_so_id')
            sale_order_line_obj = self.env['sale.order.line']
            for rec in product_ids:
                if rec.uom_id:
                    created_sol = sale_order_line_obj.create(
                        {'product_id': rec.product_id.id, 'order_id': order_id, 'product_uom': rec.uom_id.id, 'product_uom_qty': rec.qty})
                    if created_sol:
                        created_sol._onchange_product_id_warning()
        self.unlink()

    def sh_motorcycle_adv_select_btn(self):
        self.sh_motorcycle_adv_select_product(self.product_ids)

    def sh_motorcycle_adv_select_specific_btn(self):
        self.sh_motorcycle_adv_select_product(self.specific_product_ids)

    def reset_filter(self):
        if self:
            rec_dic = self.read()[0]
            if rec_dic:
                reset_vals = {'make_id': False, 'type_id': False,
                              'mmodel_id': False, 'year_id': False}
                for k, v in rec_dic.items():
                    if "x_" in k and v:
                        reset_vals.update({k: False})
                reset_vals.update({'product_attr_ids': None})
                self.product_attr_ids = None
                self.write(reset_vals)
                self._default_domain()
                self.action.update({'res_id': self.id})
        return self.action

    def reset_list(self):
        if self:
            self.product_ids = None
            self.action.update({'res_id': self.id})
        return self.action

    def reset_specific(self):
        if self:
            self.specific_product_ids = None
            self.action.update({'res_id': self.id})
        return self.action

    def filter_products(self):
        if self:
            rec_dic = self.read()[0]
            domain = []
            if self.make_id:
                domain.append(('motorcycle_ids.make_id', '=', self.make_id.id))
            if self.mmodel_id:
                domain.append(
                    ('motorcycle_ids.mmodel_id', '=', self.mmodel_id.id))
            if self.year_id:
                domain.append(('motorcycle_ids.year_id', '=', self.year_id.id))

            if rec_dic:
                for k, v in rec_dic.items():
                    if "x_" in k and "x_opt_" not in k and v:
                        pro_field_name = k.split("_", 1)[1]
                        motorcycle_field_name = "x_opt_" + pro_field_name
                        if rec_dic.get(motorcycle_field_name, False):
                            opt = rec_dic.get(motorcycle_field_name, False)
                            domain.append((pro_field_name, opt, v))
                        else:
                            # if attribute fields found
                            if "x_attr_" in k:
                                domain.append(
                                    ('product_template_attribute_value_ids', 'in', v[0]))
                            # if boolean fields found
                            else:
                                # check whether it's a
                                # selection or boolean fields or not
                                motorcycle_model_id = self.env['ir.model'].sudo().search(
                                    [('model', '=', 'motorcycle.adv.wizard')], limit=1)
                                if motorcycle_model_id:
                                    search_field = self.env['ir.model.fields'].sudo().search(
                                        [('name', '=', '' + k), ('model_id', '=', motorcycle_model_id.id)], limit=1)
                                    if search_field:
                                        if search_field.ttype in ['selection', 'boolean']:
                                            domain.append(
                                                (pro_field_name, '=', v))
                                        else:
                                            if isinstance(v, tuple):
                                                domain.append(
                                                    (pro_field_name, '=', v[0]))
                                            else:
                                                domain.append(
                                                    (pro_field_name, '=', v))
                                    else:
                                        raise UserError(
                                            _('Field not Found - ' + k))
                                else:
                                    raise UserError(
                                        _('Model not Found - motorcycle.adv.wizard'))
                    if "product_attr_ids" in k and v:
                        domain.append(
                            ('product_template_attribute_value_ids', 'in', v))
                if domain:
                    domain.append(('sale_ok', '=', True))
                    search_products = self.env['product.product'].search(
                        domain)
                    if search_products:
                        result = []
                        for product in search_products:
                            line_vals = {'product_id': product.id}
                            created_line = self.env['motorcycle.adv.wizard.product.line'].create(
                                line_vals)
                            if created_line:
                                result.append(created_line.id)
                        self.product_ids = None
                        self.product_ids = [(6, 0, result)]
                    else:
                        self.product_ids = None
                self.action.update({'res_id': self.id})
        return self.action


class MotorcycleAdvWizardProductLine(models.TransientModel):
    _name = 'motorcycle.adv.wizard.product.line'
    _description = "SO Multi Product Selection Advanced Wizard"

    motorcycle_adv_wizard_id = fields.Many2one(
        'motorcycle.adv.wizard', string='Searched Product')
    product_id = fields.Many2one('product.product', string='Product')
    default_code = fields.Char(
        related="product_id.default_code", string='Internal Reference')
    sale_price = fields.Float(
        related="product_id.list_price", string="Sale Price")
    uom_id = fields.Many2one(
        "uom.uom", related="product_id.uom_id", string="Unit of Measure")
    qty = fields.Float(string="Qty", default=1.0)

    def add_to_specific(self):
        if self and self.product_id:
            line_vals = {'product_id': self.product_id.id, 'qty': self.qty,
                         'motorcycle_adv_wizard_id_specific': self.motorcycle_adv_wizard_id.id}
            self.env['motorcycle.adv.wizard.product.line.specific'].create(
                line_vals)
            res_id = self.motorcycle_adv_wizard_id.id
            self.unlink()
            return {'name': 'Select Products Advance', 'view_mode': 'form', 'res_model': 'motorcycle.adv.wizard', 'view_id': False, 'type': 'ir.actions.act_window', 'res_id': res_id, 'target': 'new'}


class MotorcycleAdvWizardProductLineSpecific(models.TransientModel):
    _name = 'motorcycle.adv.wizard.product.line.specific'
    _description = "SO Multi Product Selection Advanced Wizard Specific"

    motorcycle_adv_wizard_id_specific = fields.Many2one(
        'motorcycle.adv.wizard', string='Searched Product')
    product_id = fields.Many2one('product.product', string='Product')
    default_code = fields.Char(
        related="product_id.default_code", string='Internal Reference')
    sale_price = fields.Float(
        related="product_id.list_price", string="Sale Price")
    uom_id = fields.Many2one(
        "uom.uom", related="product_id.uom_id", string="Unit of Measure")
    qty = fields.Float(string="Qty", default=1.0)
