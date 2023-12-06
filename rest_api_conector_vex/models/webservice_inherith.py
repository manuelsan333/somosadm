from odoo import api, fields, models
from odoo.exceptions import ValidationError

import base64
import binascii
import requests
from datetime import datetime

class  WebserviceHerencia(models.Model):
    _inherit = 'vex.web.services'
    def create_orm(self,model,data):
        #raise ValueError(str(data))

        res = self.env[str(model)].create(data)
        return res
    def write_orm(self,model,data,domain):
        d = self.env[model].search(domain)
        d.write(data)

    def delete_orm(self,model,domain):
        d = self.env[model].search(domain)
        #raise   ValidationError(d)
        d.unlink()
    def select_orm(self,model,domain):
        try:
            res = self.env[model].search(domain)
        except:
            raise ValidationError(model)
        return res

    def read_webservice_orm(self,data):
        #get model
        model = data['model']

        #get fields keys
        fields = data['fields']
        #get info fields
        fields_info = self.get_info_fields(model,fields)

        # get data
        res = self.select_orm(model, data['domain'])
        data = [] #init variable data
        #for in res
        for r in res:
            dx = {
                'id': r['id'],
            }
            #add all fields
            for f in fields:
                if f != 'id':
                    # verify if is un many2one
                    info_field = fields_info[f]
                    vx =  r[f]
                    if info_field['type'] == 'many2one':
                        vx = {
                            'id': vx['id'],
                            'display_name': vx['display_name']
                        }
                    if info_field['type'] == 'one2many':
                        vxx = []
                        for h in vx:
                            vxx.append({
                               'id': h['id'],
                               'display_name': h['display_name']
                            })
                        vx = vxx
                    if info_field['type'] == 'many2many':
                        vxx = []
                        for h in vx:
                            vxx.append({
                                'id': h['id'],
                                'display_name': h['display_name']
                            })
                        vx = vxx
                    dx[f] = vx
            data.append(dx)
        return data

    def create_webservice_orm(self,datas):
        model = datas['model']
        data  = datas['data']
        keysx, valuesx = zip(*data.items())
        keys_info = self.get_info_fields(model,keysx)
        #raise ValidationError(data)
        for d in data:
            ky = keys_info[d]
            #raise ValidationError(ky)
            if ky['type'] == 'datetime' and isinstance(data[d], str):
                data[d] = datetime.strptime(data[d], '%Y-%m-%d %H:%M:%S')
            if ky['type'] == 'date' and isinstance(data[d], str):
                data[d] = datetime.strptime(data[d], '%Y-%m-%d')
            if ky['type'] == 'binary' and isinstance(data[d], str):
                #raise ValidationError(data[d])
                try:
                    #base64.decodestring()
                    base64.b64decode(data[d])
                except binascii.Error:
                    try:
                        myfile = requests.get(str(data[d]))
                        data[d] = base64.b64encode(myfile.content)
                    except:
                        print("there is problem to dowloand the file")

            if ky['type'] == 'many2one' and isinstance(data[d], dict):
                if 'identiquer_keys' in data[d]:
                    identiquer_keysx = data[d]['identiquer_keys']
                    domainb = []
                    for i in identiquer_keysx:
                        domainb.append((i, '=', data[d]['data'][i]))
                    ty = self.select_orm(ky['relation'], domainb)
                    if ty:
                        if len(ty) == 1:
                            ty.write(data[d]['data'])
                        else:
                            raise ValidationError('more than one record was found for'+str(data[d]))
                    else:
                        ty = self.create_orm(ky['relation'],data[d]['data'])
                else:
                    ty = self.create_orm(ky['relation'], data[d]['data'])
                data[d] = ty.id

        if 'identiquer_keys' in datas:
            identiquer_keys = datas['identiquer_keys']
            domain = []
            for i in identiquer_keys:
                domain.append((i,'=',data[i]))

            res = self.select_orm(model,domain)
            if res:
                if len(res) == 1:
                    res.write(data)
                else:
                    raise ValidationError('more than one record was found')
            else:
                res = self.create_orm(model, data)

        else:
            res = self.create_orm(model, data)
        #raise ValidationError(data)

        return res

    def write_webservice_orm(self,data):
        # get model
        model = data['model']
        # get fields keys
        datax = data['data']
        # domain
        domain = data['domain']
        re = self.write_orm(model,datax,domain)
        return re

    def delete_webservice_orm(self,data):
        # get model
        model = data['model']
        domain = data['domain']
        re = self.delete_orm(model,domain)
        return re

    def test(self):
        return 'xd'

    def execute_functions_string(self,data):
        model = data['model']
        fuct = data['funcion']
        obj = self.env[model]
        funci = getattr(obj, fuct)
        return funci()





