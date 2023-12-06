from odoo import api, fields, models
from odoo.exceptions import ValidationError


class  WebserviceHerencia(models.Model):
    _inherit = 'vex.web.services'
    def get_info_fields(self,model,keys):
        fields = f'''SELECT 
                                name , ttype , relation
                             FROM ir_model_fields 
                             WHERE model = '{model}' 
                             AND name IN ('{"','".join(keys)}') '''
        #raise ValueError(fields)
        self.env.cr.execute(fields)
        fields = self._cr.fetchall()
        #raise ValueError(fields)
        fields_array = dict()
        for f in fields:
            fields_array[f[0]] = {
                'type': f[1],
                'relation': f[2]
            }
        #raise ValueError(fields_array)

        return fields_array

    def get_models_name(self):
        model = []
        for l in self.lines_resources:
            model.append(l.model_id.model)
        return model

    def get_permision_line_ws(self,model,type,compa=True):
        #raise ValidationError(self.id)
        wsl = self.env['vex.web.services.resources'].search([('model_name','=',model),('web_service_id','=',self.id)])
        if wsl['is_'+type] == compa:
            raise ValidationError('no permision  {}   in this resource'.format(type))


    def verify_token(self,token,model,type_permision):
        ws = self.env['vex.web.services'].search([('token','=',token)])
        if not ws:
            raise ValidationError('token invalid')
        if ws.method == 'all':
            return
        if ws.method == 'all-less':
            models = ws.get_models_name()
            if models:
                if model in models:
                    ws.get_permision_line_ws(model, type_permision, True)

            return
        if ws.method == 'none-less':
            models = ws.get_models_name()
            if models:
                if model in models:
                    ws.get_permision_line_ws(model, type_permision,False)
                    return
                else:
                    raise ValidationError('no permision in this resource')
        return