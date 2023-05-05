odoo.define('sh_pos_motorcycle.ProductsWidgetControlPanel', function (require, factory) {
    'use strict';

    const { useState } = owl;
    const Registries = require("point_of_sale.Registries");
    const ProductsWidgetControlPanel = require("point_of_sale.ProductsWidgetControlPanel");
    const { onMounted } = owl;

    const PosResProductsWidgetControlPanel = (ProductsWidgetControlPanel) =>
        class extends ProductsWidgetControlPanel {
            setup() {
                super.setup()
                this.state = useState({ searchWord: '' });
                this.motorcycle_results;
                onMounted(this.onMounted);
            }
            onMounted() {
                var motorcycle_types = $(document).find('#motorcycle_types')
                var motorcycle_makes = $(document).find('#motorcycle_makes')
                var motorcycle_models = $(document).find('#motorcycle_models')
                var motorcycle_years = $(document).find('#motorcycle_years')
                $(document).find('#motorcycle_make').attr({ disabled: false })
                $(document).find('#motorcycle_model').attr({ disabled: false })
                $(document).find('#motorcycle_year').attr({ disabled: false })
                if (motorcycle_types.val()) {
                    $(document).find('#motorcycle_make').attr({ disabled: false })
                }
                _.each(this.env.pos.db.motorcycle_type, function (motorcycle_type) {
                    var option = document.createElement('option')
                    motorcycle_types.append($(option).val(motorcycle_type.display_name))
                })

                _.each(this.env.pos.db.motorcycle_make, function (motorcycle_make) {
                    var option = document.createElement('option')
                    motorcycle_makes.append($(option).val(motorcycle_make.display_name))
                })

                _.each(this.env.pos.db.motorcycle_model, function (motorcycle_model) {
                    var option = document.createElement('option')
                    motorcycle_models.append($(option).val(motorcycle_model.display_name))
                })

                _.each(this.env.pos.db.motorcycle_year, function (motorcycle_year) {
                    var option = document.createElement('option')
                    motorcycle_years.append($(option).val(motorcycle_year.display_name))
                })
            }
            clearType_search(event) {
                $(document).find('#motorcycle_type').val('')
                $(document).find('#motorcycle_make').val('')
                $(document).find('#motorcycle_model').val('')
                //$(document).find('#motorcycle_make').attr({ disabled: true })
                // $(document).find('#motorcycle_makes').find('option').remove()
                //$(document).find('#motorcycle_model').attr({ disabled: true })
                // $(document).find('#motorcycle_models').find('option').remove()
                $(document).find('#motorcycle_year').val('')
                //$(document).find('#motorcycle_year').attr({ disabled: true })
                // $(document).find('#motorcycle_years').find('option').remove()
                this.trigger('clearMotorCycleSearch')
            }
            clear_make_search(event) {
                $(document).find('#motorcycle_make').val('')
                $(document).find('#motorcycle_model').val('')
                //$(document).find('#motorcycle_model').attr({ disabled: true })
                // $(document).find('#motorcycle_models').find('option').remove()
                $(document).find('#motorcycle_year').val('')
                //$(document).find('#motorcycle_year').attr({ disabled: true })
                // $(document).find('#motorcycle_years').find('option').remove()
                this.trigger('clearMotorCycleSearch')
            }
            clearModelSearch(event) {
                $(document).find('#motorcycle_model').val('')
                $(document).find('#motorcycle_year').val('')
                //$(document).find('#motorcycle_year').attr({ disabled: true })
                // $(document).find('#motorcycle_years').find('option').remove()
                this.trigger('clearMotorCycleSearch')
            }
            clearYearSearch(event) {
                $(document).find('#motorcycle_year').val('')
                this.trigger('clearMotorCycleSearch')
            }
            SearchMotorcycleType(event) {
                /**
                var motorcycle_make = $(document).find('#motorcycle_makes')
                
                console.log("motor cycle make");
                console.log(motorcycle_make);
                
                if (event.target.value != '') {
                    $(document).find('#motorcycle_make').attr({ disabled: false })
                } else {
                    this.clearType_search()
                    this.clear_make_search()
                }
                this.state.searchWord = event.target.value
                
                console.log("search word");
                console.log(this.state.searchWord);
                
                var res = this.env.pos.db.get_make_by_type(event.target.value)
                
                console.log("res fetch by type");
                console.log(res);

                _.each(res, function (each) {
                    var option = document.createElement('option')
                    var val = $(option).val(each.make_id[1])
                    var a = motorcycle_make.find('option')
                    for (var i = 0; i < a.length; i++) {
                        if ($(a[i]).val() == each.make_id[1]) {
                            $(a[i]).remove()
                        }
                    }
                    console.log("motor cycle make found");
                    console.log(val);
                    
                    motorcycle_make.append(val)
                })
                **/
            }
            SearchMotorcycleMake(event) {
                /**
                var motorcycle_model = $(document).find('#motorcycle_models')
                if (event.target.value != '') {
                    $(document).find('#motorcycle_model').attr({ disabled: false })
                } else {
                    // $(document).find('#motorcycle_models').find('option').remove()
                    this.clearModelSearch()
                }
                var type = $(document).find('#motorcycle_type').val()
                var res = this.env.pos.db.get_model_by_make_and_type(event.target.value, type)

                _.each(res, function (each) {
                    var option = document.createElement('option')
                    var val = $(option).val(each.display_name)
                    var a = motorcycle_model.find('option')
                    for (var i = 0; i < a.length; i++) {
                        if ($(a[i]).val() == each.display_name) {
                            $(a[i]).remove()
                        }
                    }
                    motorcycle_model.append(val)
                })
                **/
            }
            SearchMotorcycleModel(event) {
                /**
                var motorcycle_year = $(document).find('#motorcycle_years')
                if (event.target.value != '') {
                    $(document).find('#motorcycle_year').attr({ disabled: false })
                } else {
                    // $(document).find('#motorcycle_years').find('option').remove()
                    this.clearModelSearch()
                }
                
                console.log("--- search motor cycle model ---");
                console.log(event.target.value);
                
                var res = this.env.pos.db.get_motorcycle_by_model(event.target.value)
                this.motorcycle_results = res
                if (res.length > 0) {
                    $(document).find('#motorcycle_year').attr({ disabled: false })
                    _.each(res, function (each) {
                        if (each.year_id[1] == each.end_year_id[1]) {
                            var option = document.createElement('option')
                            var val = $(option).val(each.year_id[1])
                            motorcycle_year.append(val)
                        } else {
                            for (var i = parseInt(each.year_id[1]); i <= parseInt(each.end_year_id[1]); i++) {
                                var option = document.createElement('option')
                                var val = $(option).val(i)
                                motorcycle_year.append(val)
                            }
                        }
                    })
                }
                **/

            }
            SearchMotorcycleyear(event) {
                /**
                console.log("search event year");
                var product_lst = []
                var Products = this.env.pos.db.product_by_id;
                console.log("products are");
                console.log(Products);
                
                console.log("enable common search");
                console.log(this.env.pos.config.enable_common_search);
                
                console.log("enable search");
                console.log(this.env.pos.config.enable_search);
                
                if (this.env.pos.config.enable_common_search && this.env.pos.config.enable_search) {
                    _.each(Products, function (product) {
                        if (product.sh_is_common_product) {
                            product_lst.push(product.id)
                        }
                    })
                }
                
                console.log("motor cycle results");
                console.log(this.motorcycle_results);
                
                if (this.motorcycle_results) {
                    _.each(this.motorcycle_results, function (each) {
                        if (each) {
                            for (var i = 0; i < each.product_ids.length; i++) {
                                if (!product_lst.includes(each.product_ids[i])) {
                                    product_lst.push(each.product_ids[i])
                                }
                            }
                        }
                    })
                }
                
                console.log("final product list is");
                console.log(product_lst);
                //this.trigger('search-motorcycle', { product_ids: product_lst });
                **/
            }
            
            PerformSearch(event) {
                // type search
                var motorcycle_make = $(document).find('#motorcycle_makes');
                
                var type = $(document).find('#motorcycle_type').val();
                
                if (type != '') {
                    this.state.searchWord = type;
                    var res = this.env.pos.db.get_make_by_type(type);

                    _.each(res, function (each) {
                        var option = document.createElement('option');
                        var val = $(option).val(each.make_id[1]);
                        var a = motorcycle_make.find('option');
                        for (var i = 0; i < a.length; i++) {
                            if ($(a[i]).val() == each.make_id[1]) {
                                $(a[i]).remove()
                            }
                        }
                        motorcycle_make.append(val);
                    })
                }
                
                // makes search
                var motorcycle_model = $(document).find('#motorcycle_models');
                
                var make = $(document).find('#motorcycle_make').val();
                
                if (make != '') {
                    var res_makes = this.env.pos.db.get_model_by_make_and_type(make, type);

                    _.each(res_makes, function (each) {
                        var option = document.createElement('option');
                        var val = $(option).val(each.display_name);
                        var a = motorcycle_model.find('option');
                        for (var i = 0; i < a.length; i++) {
                            if ($(a[i]).val() == each.display_name) {
                                $(a[i]).remove();
                            }
                        }
                        motorcycle_model.append(val);
                    })
                }
                
                // model search
                //var motorcycle_year = $(document).find('#motorcycle_years');
                
                var model = $(document).find('#motorcycle_model').val();
                
                if (model != '') {
                    var res_model = this.env.pos.db.get_motorcycle_by_model(model);
                    this.motorcycle_results = res_model;
                    /* if (res_model.length > 0) {
                        _.each(res_model, function (each) {
                            if (each.year_id[1] == each.end_year_id[1]) {
                                var option = document.createElement('option');
                                var val = $(option).val(each.year_id[1]);
                                motorcycle_year.append(val);
                            } else {
                                for (var i = parseInt(each.year_id[1]); i <= parseInt(each.end_year_id[1]); i++) {
                                    var option = document.createElement('option');
                                    var val = $(option).val(i);
                                    motorcycle_year.append(val);
                                }
                            }
                        })
                    } */
                }
                
                //search year
                var product_lst = [];
                var Products = this.env.pos.db.product_by_id;
                if (this.env.pos.config.enable_common_search && this.env.pos.config.enable_search) {
                    _.each(Products, function (product) {
                        if (product.sh_is_common_product) {
                            product_lst.push(product.id);
                        }
                    })
                }
                if (this.motorcycle_results) {
                    _.each(this.motorcycle_results, function (each) {
                        if (each) {
                            for (var i = 0; i < each.product_ids.length; i++) {
                                if (!product_lst.includes(each.product_ids[i])) {
                                    product_lst.push(each.product_ids[i]);
                                }
                            }
                        }
                    })
                }
                this.trigger('search-motorcycle', { product_ids: product_lst });
            }
        }


    Registries.Component.extend(ProductsWidgetControlPanel, PosResProductsWidgetControlPanel);
    return PosResProductsWidgetControlPanel
});
