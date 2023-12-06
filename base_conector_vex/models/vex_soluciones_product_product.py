from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    id_vex_varition = fields.Char(string="ID Variation")
    vex_regular_price = fields.Float()
    stock_vex = fields.Float()
    log_meli_txt = fields.Text()

    vex_conector_ids = fields.One2many('vex.product.product.conector','product_id')
    #conectores = fields.Char(compute="get_conectores")
    #def get_conectores(self):
    #    for record in self:
    #        conectores = ''
    #        for c in record.vex_conector_ids:
    #            conectores += ' '+str(c.instance.conector)


    _sql_constraints = [
        ('unique_id_prod_vex', 'unique(id_vex_varition,active)',
         'There can be no duplication of synchronized products Variations')
    ]

    def del_id_connector_vex(self):
        self.id_vex_varition = False
        if len(self.product_tmpl_id.product_variant_ids) == 1:
            self.product_tmpl_id.id_vex = False
            self.product_tmpl_id.conector = False
            self.product_tmpl_id.server_vex = False

    @api.depends('list_price', 'price_extra')
    def _compute_product_lst_price(self):
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse([self._context['uom']])
        for product in self:
            if to_uom:
                list_price = product.uom_id._compute_price(product.list_price, to_uom)
            else:
                list_price = product.list_price
            api_precio = product.vex_regular_price
            if api_precio:
                product.lst_price = api_precio
            else:
                product.lst_price = list_price + product.price_extra

    def update_conector_vex(self,wizard=True):
        return


    def stock_vex_conector(self,server):
        self.env['vex.synchro'].check_synchronize(server)
        stock = 0
        type_stock = server.type_stock_export or 'hand'
        if type_stock in ['hand','available'] :
            domain_quant = self.action_open_quants()['domain']
            quant = self.env['stock.quant'].search(domain_quant)
            stock = 0
            if quant:
                for qua in quant:
                    if qua.location_id.warehouse_id == server.warehouse_stock_vex:
                        if server.location_excluded:
                            if qua.location_id.id in server.location_excluded.ids:
                                continue
                        if type_stock == 'hand':
                            stock += qua.quantity
                        if type_stock == 'available':
                            stock += qua.available_quantity

        if type_stock == 'forecast':
            warehouse_x_export = server.warehouse_stock_vex
            data = self.env['report.stock.report_product_product_replenishment'].with_context(
                warehouse=warehouse_x_export.id)._get_report_data(False, [self.id])
            future_virtual_available = data['virtual_available']

            if future_virtual_available < server.export_stock_min:
                future_virtual_available = 0

            stock = future_virtual_available

        return stock

    #########################
    def _get_display_price_meli(self, product,pricelist_id,datex,server_vex,qty):
        # TO DO: move me in master/saas-16 on sale.order
        # awa: don't know if it's still the case since we need the "product_no_variant_attribute_value_ids" field now
        # to be able to compute the full price

        # it is possible that a no_variant attribute is still in a variant if
        # the type of the attribute has been changed after creation.
        #no_variant_attributes_price_extra = [
        #    ptav.price_extra for ptav in self.product_no_variant_attribute_value_ids.filtered(
        #        lambda ptav:
        #        ptav.price_extra and
        #        ptav not in product.product_template_attribute_value_ids
        #    )
        #]
        #if no_variant_attributes_price_extra:
        #    product = product.with_context(
        #        no_variant_attributes_price_extra=tuple(no_variant_attributes_price_extra)
        #    )

        #if pricelist_id.discount_policy == 'with_discount':
        #    return product.with_context(pricelist=pricelist_id.id, uom=product.uom_id).price
        product_context = dict(
            self.env.context,
            #partner_id=self.order_id.partner_id.id,
            date=datex,
            uom=product.uom_id
        )

        final_price, rule_id = pricelist_id.with_context(product_context).get_product_price_rule(
            product or self.product_id, self.product_uom_qty or 1.0, self.env.company.partner_id)
        base_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id,
                                                                                           self.product_uom_qty,
                                                                                           self.product_uom,
                                                                                           pricelist_id.id)
        if currency != pricelist_id.currency_id:
            base_price = currency._convert(
                base_price, pricelist_id.currency_id,
                server_vex.company  or self.env.company, datex or fields.Date.today())
        # negative discounts (= surcharge) are included in the display price
        return max(base_price, final_price)

