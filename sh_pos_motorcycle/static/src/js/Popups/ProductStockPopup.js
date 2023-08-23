odoo.define('sh_pos_motorcycle.ProductStockPopup', function(require) {
    'use strict';
    
    const Registries = require("point_of_sale.Registries");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");

    class ProductStockPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }
    }
    ProductStockPopup.template = 'ProductStockPopup'

    Registries.Component.add(ProductStockPopup)

    return ProductStockPopup
});