from odoo import api, fields, models

class VexRestapilist(models.Model):
    _name                = "vex.restapi.list"
    _description         = "List Vex RestApi"
    name                 = fields.Char(required=True)
    argument             = fields.Char()
    model                = fields.Char()
    log                  = fields.One2many('vex.logs','vex_list')
    interval             = fields.Integer(default=60)
    interval_type        = fields.Selection([('minutes', 'Minutes'),('hours', 'Hours'),
                                      ('days', 'Days'),('weeks', 'Weeks'),('months', 'Months')],default='minutes')
    active_cron          = fields.Boolean(default=False)
    interval_stock       = fields.Integer(default=60)
    interval_type_stock  = fields.Selection([('minutes', 'Minutes'), ('hours', 'Hours'),
                                      ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], default='minutes')
    active_cron_stock    = fields.Boolean(default=False)
    automatic            = fields.Boolean()
    total_count          = fields.Integer(compute='_generate_count')
    next_date_cron       = fields.Datetime(compute='_generate_next_date',string="Next Execution Date")
    next_date_cron_stock = fields.Datetime(compute='_generate_next_date_stock', string="Next Execution Date")
    export               = fields.Boolean()
    importv              = fields.Boolean()
    per_page = fields.Integer(default=10, required=True,
                              string="Items per page")
    all_items = fields.Boolean(default=True)
    max_items = fields.Integer(string="Maximum number of items to be returned approximately")

    import_by_parts = fields.Boolean()
    conector             = fields.Selection([])
    stock_import = fields.Boolean()
    import_images = fields.Boolean()
    import_images_website = fields.Selection([('save','Save url'),('dowload','Save url and Dowload')])
    limit_action = fields.Integer(default=80)
    last_number_import = fields.Integer(default=0,string="Ultima Cantidad Importada")



    _sql_constraints = [
        ('unique_id_argument', 'unique(argument,conector)', 'There can be no duplication of argument in conector')
    ]

    #funcion  para cambiar las facturas el customer los apuntes contables

    def go_export_product(self):
        view = self.env.ref('stock.stock_product_normal_action').read([])[0]
        view['domain'] = f"[('id_vex_varition','=',False)]"
        view['limit'] = self.limit_action
        # model = 'product.product'

        return view

    def change_lines_customer(self,domain):
        orders = self.env['sale.order'].search(domain)
        for o in orders:
            for i in o.invoice_ids:
                if i.partner_id.type == 'invoice':
                    parent = i.partner_id.parent_id if i.partner_id.parent_id else i.partner_id

                    self.env.cr.execute(f'''UPDATE account_move SET partner_id = {parent.id} WHERE id = {i.id}''')
                    self.env.cr.execute(f'''UPDATE account_move_line SET partner_id = {parent.id} WHERE move_id = {i.id}''')
                continue

    def go_action_list(self):

        model = str(self.model)

        domain = "[('conector','=','{}')]".format(self.conector)

        view_mode = 'tree,kanban,form'
        if self.argument ==  'products':
            view_mode = 'kanban,tree,form'




        if self.argument == 'fee':
            domain = "[('conector','=','{}'), ('id_vex', '!=', False),('type', '=', 'service')]".format(self.conector)

        if str(self.model) == 'product.template':
            view = self.env.ref('stock.stock_product_normal_action').read([])[0]
            view['domain'] = f"[('vex_conector_ids.instance.conector','=','{self.conector}')]"
            #view['domain'] = f"[('vex_conector_ids','!=',False)]"
            view['limit'] = self.limit_action
            #model = 'product.product'

            return view

        if str(self.model) == 'sale.order':

            #self.change_lines_customer([('conector','=',self.conector)])
            view = self.env.ref('sale.action_orders').read([])[0]
            view['domain'] = domain
            view['limit'] = self.limit_action

            return view
        dx =  {
            'name': str(self.name),
            'type': 'ir.actions.act_window',
            'res_model': model,
            'view_mode': view_mode,
            'view_type': 'form',
            'domain': domain,
            'limit': self.limit_action
        }




        return dx

    def go_action_products(self):
        return {
            'name': 'Products '+str(self.conector),
            'type': 'ir.actions.act_window',
            'res_model': 'product.template',
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'domain': "[('conector','=','{}')]".format(self.conector)
        }

    def stop_sync(self):
        return
        '''
        update_cron = "UPDATE ir_cron SET active = 'f'  WHERE argument = 'vex_cron' ".format(server.id)
        self.env.cr.execute(update_cron)
        '''
        cron = self.env['ir.cron'].search([('argument','=',str(self.argument)),('conector', '!=', False),
                                               ('automatic','=',True)])
        if cron:
            cron.active = False


    def _generate_next_date(self):
        cron = self.env['ir.cron'].search([('argument', '=', str(self.argument)),('conector', '!=', False),('automatic','=',False),
                                           "|",
                                           ("active", "=", True), ("active", "=", False)])
        if cron:
            self.next_date_cron = cron.nextcall
        else:
            self.next_date_cron = None
    def _generate_next_date_stock(self):
        cron = self.env['ir.cron'].search([('argument', '=', 'stock'),('conector', '!=', False),('automatic','=',False),
                                           "|",
                                           ("active", "=", True), ("active", "=", False)])
        if cron:
            self.next_date_cron_stock = cron.nextcall
        else:
            self.next_date_cron_stock = None

    #@api.model
    def _generate_count(self):
        for record in self:
            #buscar la cantidad
            model = record.model
            if model:
                count = self.env[str(model)].search_count([('conector', '=', str(record.conector)),('id_vex', '!=', False)])

                argument = record.argument
                if argument == 'products':
                    #view[
                    #    'domain'] = f"[('conector','=','{self.conector}'),('id_vex', '!=', False),('id_vex_varition','!=',False)]"
                    #f"[('vex_conector_ids.instance.conector','=','{self.conector}')]"
                    count = self.env['product.product'].search_count([('vex_conector_ids.instance.conector','=',f"'{record.conector}'")])
                if argument == 'fee':
                    count = self.env[str(model)].search_count([('conector', '=', str(record.conector)),('id_vex', '!=', False),
                                                               ('detailed_type','=','service')])

                if argument == 'images':
                    count = self.env[str(model)].search_count(
                        [('conector', '=', str(record.conector))])


                record.total_count = count

            else:
                record.total_count = 0