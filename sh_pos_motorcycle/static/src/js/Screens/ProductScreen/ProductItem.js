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
            }
            
            ClickOnDetails(event) {
                var self = this
                const Product = event.detail
                var motorcycle_id = Product.motorcycle_ids
                var specification_line = Product.specification_lines

                console.log("evento");
                console.log(event);
                console.log("product loaded");
                console.log(Product);

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
                this.showPopup('ProductDetailsPopup', {
                    details: details,
                    product: Product.name,
                    specs: specs,
                })

            }
        }

    Registries.Component.extend(ProductItem, PosProductItem);
    return PosProductItem
});
