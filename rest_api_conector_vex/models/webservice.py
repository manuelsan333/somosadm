from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import string
import secrets
import time
class WebServices(models.Model):
    _name                = "vex.web.services"
    _description         = "Web Services Vex"
    name                 = fields.Char(required=True)
    token                = fields.Char()
    token_related        = fields.Char(compute='get_token_related',string='Token')
    @api.depends('token')
    def get_token_related(self):
        for record in self:
            lg = len(record.token) if record.token else 0
            lg = lg - 1 if lg > 0 else 0
            token_related = str(self.token)[:1] if self.token else self.token
            for r in range(lg):
                token_related = token_related +"*"

            self.token_related = token_related
    method               = fields.Selection([('all','All Permission'),
                                             ('all-less','All Permission less'),
                                             ('none-less','No permission except')],required=True)
    lines_resources      = fields.One2many('vex.web.services.resources','web_service_id')

    def generate_key(self):
        if not self.id:
            raise ValidationError('deberías guardar el cambio primero')
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(45))
        password = password + str(self.id)
        self.write({'token': password})
        return {
            'name': ('token generated , save this please!!, it not show again'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'vex.wizard.popup',
            'target': 'new',

            'context': dict(
                default_msg = password,
            ),
        }

    def json_execute_create(self, table, data):
        table = str(table).replace('.', '_')
        filas_create = ''
        values_create = ''
        for d in data:
            filas_create = filas_create + ', ' + str(d)
            values_create = values_create + ', ' + str(data[d])
        filas_create = filas_create[1:]
        values_create = values_create[1:]
        create = "INSERT INTO  {tabla} ({filas}) VALUES ({values}) ;".format(tabla=table,
                                                                             filas=filas_create,
                                                                             values=values_create)
        self.env.cr.execute(create)
        return True
        #return self._cr.fetchall()


    def json_execute_update(self, table, data, id):
        table = str(table).replace('.', '_')
        set_update = ''
        for d in data:
            set_update = set_update + ', ' + str(d) + '=' + str(data[d])
        set_update = set_update[1:]
        write = "UPDATE {tabla} set  {set} where id = {id_vex} ;".format(tabla=table, set=set_update, id_vex=id)
        #raise ValidationError(write)
        self.env.cr.execute(write)
        #return self._cr.fetchall()

    def UnionWithoutRepetition(self,lst1, lst2):
        final_list = list(set(lst1) | set(lst2))
        return final_list

    def array_to_join_string(self,data,separator=','):
        keys = []
        values = []
        if not separator:
            raise ValueError("separator  can't be empty")
        separator = ' {} '.format(separator)
        for d in data:
            keys.append(str(d))
            values.append(str(data[d]))

        keys = separator.join(keys)
        values = separator.join(values)
        return keys , values



    def array_to_join_sql(self,data,model,identiquer_keys=None):
        keys = keys_update = []
        for k in data:
            keysx, valuesx = zip(*k.items())
            #concatenar los keys
            keys = self.UnionWithoutRepetition(keys,keysx)
            if identiquer_keys:
                arq = []
                for i in k:
                    if i in identiquer_keys:
                        strx = ' {} = {} '.format(i,k[i])
                        arq.append(strx)
                addx = ' AND '.join(arq)
                addx = "( {} )".format(addx)
                keys_update.append(addx)
                        #raise ValueError('yeii')
        #raise ValueError(keys_update)

        # get fields' informations
        fields_array = self.get_info_fields(model, keys)
        values = ''
        queryx = "(#{}#)".format('#,#'.join(keys))
        for k in data:
            #keysx, valuesx = zip(*k.items())
            dx = queryx
            for d in k:
                #raise ValueError(data)
                vx = self.convert_field_insertable(fields_array[d],k[d],fields_array)
                d = "#{}#".format(d)
                dx = dx.replace(d, vx)
            for k in keys:
                k = "#{}#".format(k)
                dx = dx.replace(k,'NULL')
            values = values + "," + dx

        return ','.join(keys) , values[1:]



    def convert_field_insertable(self,field_info,value,array_fields):
        type_field = field_info['type']
        #conditions for verify the type fields
        if type_field in ('text', 'char', 'date', 'date_time', 'html', 'selection', 'text'):
            value = str(value)
        if type_field in ('boolean'):
            if isinstance(value, bool):
                value = 't' if value else 'f'
                #raise ValueError(value)
            else:
                msg = f'''{str(value)} not is  boolean'''
                raise ValueError(msg)
        if type_field in ('many2one'):
            if  isinstance(value, dict):
                if not 'identiquer_keys' in value:
                    msg = f'''{str(value)}  haven't identiquer_keys '''
                    raise ValueError(msg)
                model = field_info['relation']
                data = value['data']
                datax = {
                    'model': model,
                    'data': [data],
                    'identiquer_keys': value['identiquer_keys']
                }
                #raise ValueError(str(datax))
                self.create_update(datax)
                domain = []
                for dxt in value['identiquer_keys']:
                    key = dxt
                    valu = data[dxt]
                    domain.append((key,'=',valu))
                d = self.env[model].search(domain)
                #raise ValueError(d)
                value = d.id

            else:
                if not (isinstance(value, int) or isinstance(value, str)) :
                    msg = f'''{str(value)} is  incompatible with  type field'''
                    raise ValueError(msg)


        value = "'{}'".format(value)
        return value


    def select(self,model,table,header=None,where=None):
        header = '*' if not header else ' , '.join(header)
        select = f'''SELECT 
                        '{header}'
                      FROM '{table}'  '''
        if where:
            select += f'''
              WHERE model = '{model}' 
                      AND name IN {tuple(where)}
            '''


        return select



    def create_update(self,datas,create_constraint=True):
        data = datas['data']
        modelx = datas['model']
        identiquer_keys = datas['identiquer_keys'] if  'identiquer_keys' in datas else None
        if not data:
            raise ValueError('data empty')
        table = modelx.replace('.','_')
        query = None
        keys , values = self.array_to_join_sql(data,modelx,identiquer_keys)
        if not 'identiquer_keys' in datas:
            query = '''
                    INSERT INTO {table} ({keys})
                    VALUES 
                       {values} ;
                    '''.format(table=table,keys=keys,values=values)

            # when is product_template


        else:
            keys_updatex = ' , '.join(tuple(identiquer_keys))
            update_set = []
            keysx = keys.split(',')
            for k in keysx:
                qy = ' {key} = EXCLUDED.{key} '.format(key=k)
                update_set.append(qy)
            update_set = ' , '.join(update_set)

            query = ''
            if create_constraint:
                unix = str(time.time())
                unix = unix.replace('.', '_')
                name_constraint = 'vex_' + unix + str('_'.join(tuple(identiquer_keys)))
                query += f'''
                            ALTER TABLE {table} DROP CONSTRAINT IF EXISTS {name_constraint};
                            ALTER TABLE  {table}
                            ADD CONSTRAINT {name_constraint}
                            UNIQUE  ({keys_updatex});
            
                '''

                #raise ValidationError(query)

            query += '''
                        INSERT INTO {table} ({keys})
                        VALUES 
                          {values} 
                        ON CONFLICT ({keys_update}) DO UPDATE SET 
                           {update_set} ;
                                '''.format(table=table, keys=keys, values=values ,
                                           keys_update=keys_updatex, update_set = update_set)
            if create_constraint:
                query += f'''
                                        alter table {table}
                                        drop constraint {name_constraint};
                                        '''




        if modelx == 'product.template':
            query += '''
                         INSERT INTO product_product (product_tmpl_id,active,default_code)
                           SELECT PT.id as product_tmpl_id , PT.active , PT.default_code as active FROM product_template PT
                           WHERE 
                           (SELECT COUNT(*) FROM product_product WHERE product_tmpl_id = PT.id) <= 0 ;
                    '''

        #if modelx == 'product.category':
        #    query += '''
        #                UPDATE product_category
        #                SET  parent_path =  ( id ||'/')
        #                WHERE parent_path IS NULL AND parent_id IS NULL ;
        #                UPDATE product_category c1
        #                SET  parent_path =  ( c2.parent_path  || '/' ||  c1.id || '/')
        #                FROM product_category c2
        #                WHERE c1.parent_id  =  c2.id AND c1.parent_path IS NULL ;
        #             '''

        if 'execute_query_end' in datas:
            query += datas['execute_query_end']



        #raise ValidationError(query)


        self.env.cr.execute(query)
        return True


class WebServicesResources(models.Model):
    _name = "vex.web.services.resources"
    _description = "Web Services Vex Resources"
    web_service_id = fields.Many2one('vex.web.services',required=True)
    model_id = fields.Many2one('ir.model',required=True,string="Resource",ondelete='set default')
    model_name = fields.Char(related='model_id.model')
    is_read = fields.Boolean(string="Read")
    is_write = fields.Boolean(string="Write")
    is_create = fields.Boolean(string="Create")
    is_unlink = fields.Boolean(string="Unlink")