odoo.define('sh_pos_motorcycle.ProductsWidget', function (require) {
    'use strict';

    const ProductsWidget = require("point_of_sale.ProductsWidget");
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require("point_of_sale.Registries");
    var utils = require('web.utils');
    const { onMounted } = owl;

    const PosProductsWidget = (ProductsWidget) =>
        class extends ProductsWidget {
            constructor() {
                super(...arguments);
                if (this.env.pos.config.enable_search) {
                    $('.pos-rightheader').addClass('sh_main_right_header')
                    $('.pos-topheader').addClass('sh_topheader')
                }
            }
            setup() {
                super.setup()
                useListener('search-motorcycle', this._motorcycles);
                useListener('clearMotorCycleSearch', this._clearMotorCycleSearch);
                onMounted(this.onMounted);
            }
            onMounted() {
                if (this.env.pos.config.sh_hide_search_bar_for_mobile) {
                    if ($('.sh_search_box')) {
                        _.each($('.sh_search_box'), function (each_serach_bar) {
                            $(each_serach_bar).addClass('sh_hide_search')
                        })
                    }
                }
            }
            _clearMotorCycleSearch() {
                this.autopart_ids = []
                this.render()
            }
            _motorcycles(event) {
                this.autopart_ids = event.detail.product_ids
                this.productsToDisplay
                this.render()
            }
            get productsToDisplay() {
                var res = []
                var self = this
                var list = []
                if (this.env.pos.config.enable_search) {
                    if (this.searchWord !== '') {
                        if ($('#motorcycle_year').val()) {
                            return self.env.pos.db.search_product_in_motorcycle(self.selectedCategoryId, self.searchWord)
                        } else {
                            return this.env.pos.db.search_product_in_category(
                                this.selectedCategoryId,
                                this.searchWord
                            );
                        }
                    } else if (this.autopart_ids) {
                        var rec = this.env.pos.db.get_product_by_motorcycle(this.autopart_ids)
                        var search_string;
                        var data =''
                        _.each(rec, function (i) {
                            if (i) {
                                search_string = utils.unaccent(self.env.pos.db._product_search_string(i));
                                if(self.env.pos.db.produt_search_string[self.selectedCategoryId] === undefined){
                                    self.env.pos.db.produt_search_string[self.selectedCategoryId] = '';
                                }
                                data = data+search_string
                                res.push(i)
                            }
                        })
                        self.env.pos.db.produt_search_string[self.selectedCategoryId] = data
                        if (res.length > 0) {
                            return res
                        } else {
                            return this.env.pos.db.get_product_by_category(this.selectedCategoryId)
                        }
                    }
                    else {
                        list = this.env.pos.db.get_product_by_category(this.selectedCategoryId);
                        return list.sort(function (a, b) { return a.display_name.localeCompare(b.display_name) });
                    }
                } else {
                    return super.productsToDisplay
                }
            }
        }

    Registries.Component.extend(ProductsWidget, PosProductsWidget);
});
