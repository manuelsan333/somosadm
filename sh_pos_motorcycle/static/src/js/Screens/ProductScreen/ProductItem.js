odoo.define('sh_pos_motorcycle.ProductItem', function (require, factory) {
    'use strict';

    const ProductItem = require("point_of_sale.ProductItem");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");

    const PosProductItem = (ProductItem) =>
        class extends ProductItem {
            constructor() {
                super(...arguments)
            }
            setup(){
                super.setup();
                useListener('click_on_detail', this.ClickOnDetails);
                useListener('click_on_stock', this.ClickOnStock);
            }
            
            ClickOnDetails(event) {
                var self = this
                const Product = event.detail
                var motorcycle_id = Product.motorcycle_ids
                var specification_line = Product.specification_lines

                var details = []
                var specs = []

                _.each(motorcycle_id, function (each_motorcycle) {
                    var res = self.env.pos.db.get_motorcycle_by_id(each_motorcycle)
                    details.push(res)
                })

                _.each(specification_line, function (each_spec) {
                    var res = each_spec.id
                    specs.push(res)
                })

                // product location
                var stock_loc = []
                if (Product.id in self.env.pos.db.stockLocationsById) {
                    stock_loc = self.env.pos.db.stockLocationsById[Product.id];
                }
                console.log(Product);
                
                this.showPopup('ProductDetailsPopup', {
                    details: details,
                    specs: specs,
                    stock_loc: stock_loc,
                })

            }

            ClickOnStock(event) {
                var self = this
                const Product = event.detail
                this.showPopup('ProductStockPopup', {
                    stock_loc: []
                })
            }
        }

    Registries.Component.extend(ProductItem, PosProductItem);
    return PosProductItem
});
