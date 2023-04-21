odoo.define("sh_pos_order_warehouse.models", function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require("point_of_sale.Registries"); 

    const shMotorCycleosGlobalState = (PosGlobalState) => class shMotorCycleosGlobalState extends PosGlobalState {

        async _processData(loadedData) {
            await super._processData(...arguments);
            var self = this
            var  MototrcycleType = loadedData['motorcycle.type'] || [];
            if(MototrcycleType){
                _.each(MototrcycleType, function (type) {  
                    self.db.motorcycle_type.push(type)
                })
            }

            var  Mototrcyclemake = loadedData['motorcycle.make'] || [];
            if(Mototrcyclemake){
                _.each(Mototrcyclemake, function (make) {  
                    self.db.motorcycle_make.push(make)
                    self.db.motorcycle_make_by_id[make.id] = make
                })
            }

            var  Mototrcyclemodel = loadedData['motorcycle.mmodel'] || [];
            if(Mototrcyclemodel){
                _.each(Mototrcyclemodel, function (model) {  
                    self.db.motorcycle_model.push(model)
                    self.db.motorcycle_model_by_id[model.id] = model
                })
            }

            var all_motorcycle = loadedData['motorcycle.motorcycle'] || [];
            if(all_motorcycle){
                _.each(all_motorcycle, function (motorcycle) {  
                    self.db.all_motorcycle.push(motorcycle)
                })
            }

            var  MotorcycleYear = loadedData['motorcycle.year'] || [];
            if(MotorcycleYear){
                _.each(MotorcycleYear, function (motorcycle_year) {  
                    self.db.motorcycle_year.push(motorcycle_year)
                    self.db.motorcycle_year_by_id[motorcycle_year.id] = motorcycle_year
                })
            }

            var  productSpecs = loadedData['sh.product.specification'] || [];
            if(productSpecs){
                console.log("specs loaded");
                _.each(productSpecs, function (spec) {  
                    console.log(spec.name + ": " + spec.value);
                })
            }
        }
        
    }

    Registries.Model.extend(PosGlobalState, shMotorCycleosGlobalState);
});
