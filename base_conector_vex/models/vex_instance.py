from odoo import api, fields, models
import requests
from odoo.exceptions import UserError
import datetime
from datetime import timedelta
class VexInstance(models.Model):
    _name        = "vex.instance"
    _description = "Instance Vex"
    name = fields.Char(string='Name', required=True)
    company = fields.Many2one('res.company')
    picking_policy = fields.Selection([('direct', 'Deliver each product when available'),
                                       ('one', 'Deliver all products at once')], default='direct')
    warehouse = fields.Many2one('stock.warehouse')
    type_stock_export = fields.Selection([('hand','A mano'),('available','Disponible'),('forecast','Pronosticado')],
                                         string="Tipo de Stock (exportar)",required=True,default='hand')
    location_id = fields.Many2one('stock.location', string="Stock Location",related="warehouse.lot_stock_id")


    journal_id = fields.Many2one('account.journal',string="Diario")
    payment_term = fields.Many2one('account.payment.term')
    use_date_specific = fields.Boolean(string="Usar Fecha Especifica")
    latest_days_order = fields.Integer(string="Ultimos N dias")
    order_after = fields.Datetime()
    order_after_days = fields.Datetime(compute="get_order_after_days")
    logs_general = fields.Html()
    def get_order_after_days(self):
        for record in self:
            record.order_after_days = fields.Datetime.now() -timedelta(days=record.latest_days_order)

    all_orders = fields.Boolean(defaul=True)
    all_status_orders = fields.Boolean(defaul=True, string='All the states')
    total_products = fields.Integer(compute='_generate_total')
    total_categories = fields.Integer(compute='_generate_total')
    total_customers = fields.Integer(compute='_generate_total')
    total_orders = fields.Integer(compute='_generate_total')
    conector = fields.Selection([])
    categ_id = fields.Many2one('product.category', string="product category")
    active_automatic = fields.Boolean(default=False, string="Activate automatic sync")

    pricelist = fields.Many2one('product.pricelist')
    sales_team = fields.Many2one('crm.team', string="Sales Team")

    import_lines = fields.One2many('vexlines.import','instance')


    sequence_id = fields.Many2one('ir.sequence')
    use_sequence_order = fields.Boolean(string="Usar Secuencia")
    prefix_sequence = fields.Char(string="Prefijo de la Secuencia Orden")

    state_orders = fields.One2many('vex.instance.status.orders','instance')

    import_stock = fields.Boolean(default=True)
    url_license = fields.Char(default='https://www.pasarelasdepagos.com/', required=True)
    license_secret_key = fields.Char(default='587423b988e403.69821411')
    license_key = fields.Char()
    active_list = fields.Many2one('vex.restapi.list')
    search_sku = fields.Boolean(default=True)
    tax_id = fields.Many2one('account.tax',string='Impuesto')
    use_tax_product = fields.Boolean(default=False,string="Usar el Impuesto del producto")
    update_price = fields.Boolean(default=True,string="Exportar Precio a Mercado Libre")
    update_stock = fields.Boolean(default=True,string="Exportar Stock a Mercado Libre")
    update_title = fields.Boolean()
    update_description = fields.Boolean(default=True, string="Actualizar Descripcion")
    medium_id = fields.Many2one('utm.medium',string="Medio")

    last_number_import = fields.Integer(default=0, string="Ultima Cantidad Orden Importada")
    verify_albaranes = fields.Boolean(default=True,string="Verificar Albaranes")
    create_not_exists = fields.Boolean(string="Crear Productos No Existentes")
    product_payment_add =  fields.Many2one('product.product',string="Producto Dinero Agregado")

    print_data_with_error = fields.Boolean(string="Imprimir El dato como Error")
    print_shipping_with_error = fields.Boolean(string="Imprimir El envio como Error")
    sku_suppress = fields.Text(string="Suprimir Termino Busqueda del Sku")





    discount_fee = fields.Selection([
        ('save','Guardar como Dato'),
        ('save_line','Guardar como Linea')
    ],string="Comision"
    )

    shipment = fields.Selection([
        ('save','Guardar como Dato'),
        ('save_line','Guardar como Linea')
    ],string="Envio"
    )

    user_sale_id = fields.Many2one('res.users',string="Vendedor Ventas")
    export_stock_min = fields.Integer(string="Stock Minimo a exportar")
    share_multi_instances = fields.Boolean(default=False,string="Compartir Productos entre cuentas")
    export_stock_all_products = fields.Boolean(default=True,string="Exportar  todos los productos")
    warehouse_stock_vex = fields.Many2one('stock.warehouse', string="Almacen x Exportar")
    type_document = fields.Many2one('l10n_latam.identification.type',string="Tipo de Identificacion")
    description_company = fields.Text(string="Descripcion Empresa",default='')
    include_name_init_descripton = fields.Boolean(default=True,string="Incluir Nombre del Producto al incio de la descripcion")
    search_archive_products = fields.Boolean(default=False,string="Buscar Productos Archivados")
    import_categories = fields.Boolean(string="Importar Categorias")
    id_external_aditional_order = fields.Many2one('ir.model.fields',
                                                  string='ID MELI EXTERNO VALIDACION',
                                                  domain=[('model_id.model','=','sale.order'),('ttype','=','char')])
    product_shipment = fields.Many2one('product.product', string="Producto x Envio")
    location_excluded = fields.Many2many('stock.location',string="Ubicaciones Excluidas")

    products_reemplace = fields.One2many('vex.instance.product.reemplace', 'instance')
    import_adress_in_fields = fields.Boolean(string="Importar datos de la direccion en los campos",default=True)


    def update_lines_taxes(self):
        lines  = self.env['sale.order.line'].search([('order_id.id_vex','!=',False)])
        c = 0

        for line in lines:
            if c == 1000:
                break
            for tax in line.tax_id:
                if tax.id != self.tax_id.id:
                    line.tax_id = [(6,0,[self.tax_id.id])]
                    c += 1
                    #raise ValueError(line.tax_id[0].name)
                    #break

        #raise ValueError(lines)

    def get_crons(self):
        return
    def validate_licence(self):
        URL = f"https://www.pasarelasdepagos.com?license_key={self.license_key}&slm_action=slm_check&secret_key={self.license_secret_key}"
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        try:
            r = requests.get(url=URL, headers=headers).json()
        except requests.exceptions.ConnectionError as errrt:
            return

        #raise ValueError(str(r))
        if not 'result' in r:
            return
            raise UserError(str(r))
        if r['result'] != 'success':
            raise UserError('NO TINES LECENCIA VALIDA')
        if r['status'] != 'active':
            raise UserError('LA LICENCIA NO ESTA ACTIVA')

    @api.model
    def default_get(self,fields):
        res = super(VexInstance,self).default_get(fields)
        sq = self.env['ir.sequence'].search([('code','=','sale.order')],limit=1)
        if sq:
            res.update({'sequence_id': sq.id})
        return res

    def _generate_total(self):
        for record in self:
            # buscar todos los productos para este servidor
            products = self.env['product.template'].search_count(
                [('id_vex', '!=', False), ('server_vex', '=', int(record.id))])
            record.total_products = products
            # categories = self.env['product.public.category'].search_count([(id_api, '!=', False), (server_api, '=', int(record.id))])
            record.total_categories = 0
            # customers = self.env['res.partner'].search_count([(id_api, '!=', False), (server_api, '=', int(record.id))])
            record.total_customers = 0
            # orders = self.env['sale.order'].search_count([(id_api, '!=', False), (server_api, '=', int(record.id))])
            record.total_orders = 0

    def fun_test(self):
        self.validate_licence()
        return 0

    def stop_sync(self):
        cron = self.env['ir.cron'].search([('argument', '=', 'vex_cron'),
                                           "|",
                                           ("active", "=", True), ("active", "=", False)])
        if cron:
            cron.active = False

    def view_setting_sinc_lines(self):
        cron = self.env['ir.cron'].search([('argument', '=', 'vex_cron'),
                                           "|",
                                           ("active", "=", True), ("active", "=", False)])

        view = self.env.ref('base.ir_cron_view_form', False)

        # picking_type_id = self.picking_type_id or self.picking_id.picking_type_id
        return {
            'name': ('Configurar Cron'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'ir.cron',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'current',
            'res_id': cron.id,
            'context': dict(
                cron.env.context,
            ),
        }

        return

    class VexImportLines(models.Model):
        _name = "vexlines.import"
        url = fields.Char(required=True)
        orden = fields.Integer(required=True)
        instance = fields.Many2one('vex.instance',required=True)
        accion = fields.Many2one('vex.restapi.list',required=True)
        state = fields.Selection([('done','Realizado'),('wait','Pendiente')],default="wait")



