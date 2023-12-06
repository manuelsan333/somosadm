from odoo import http
#from odoo.http import request
import logging
import pprint
_logger = logging.getLogger(__name__)

class WebHooks(http.Controller):
    @http.route(['/vex_api_rest'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_api(self,**post):
        data = http.request.jsonrequest

        #_logger.info('OKKK', pprint.pformat(data))
        #return data
        return http.request.env['vex.web.services'].sudo().create_update(data)

    @http.route(['/read_apivex'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_read(self, **post):
        data = http.request.jsonrequest
        # _logger.info('OKKK', pprint.pformat(data))
        # return data
        headers = http.request.httprequest.headers
        token = headers['token']
        http.request.env['vex.web.services'].sudo().verify_token(token, str(data['model']), 'read')
        return http.request.env['vex.web.services'].sudo().read_webservice_orm(data)

    @http.route(['/create_apivex'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_create(self, **post):
        data = http.request.jsonrequest
        headers = http.request.httprequest.headers
        token =  headers['token']
        http.request.env['vex.web.services'].sudo().verify_token(token,str(data['model']),'create')
        return http.request.env['vex.web.services'].sudo().create_webservice_orm(data)

    @http.route(['/write_apivex'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_write(self, **post):
        data = http.request.jsonrequest
        headers = http.request.httprequest.headers
        token = headers['token']
        http.request.env['vex.web.services'].sudo().verify_token(token, str(data['model']), 'write')
        return http.request.env['vex.web.services'].sudo().write_webservice_orm(data)

    @http.route(['/delete_apivex'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_delete(self, **post):
        data = http.request.jsonrequest
        headers = http.request.httprequest.headers
        token = headers['token']
        http.request.env['vex.web.services'].sudo().verify_token(token, str(data['model']), 'unlink')
        return http.request.env['vex.web.services'].sudo().delete_webservice_orm(data)

    @http.route(['/execute_apivex'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def index_execute(self, **post):
        data = http.request.jsonrequest
        return http.request.env['vex.web.services'].sudo().execute_functions_string(data)