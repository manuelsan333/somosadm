odoo.define('sh_pos_motorcycle.ProductDetailsPopup', function(require) {
    'use strict';
    
    const Registries = require("point_of_sale.Registries");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");

    class ProductDetailsPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
    }
    ProductDetailsPopup.template = 'ProductDetailsPopup'

    Registries.Component.add(ProductDetailsPopup)

    return ProductDetailsPopup
});
