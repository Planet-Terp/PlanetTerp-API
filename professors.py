import web
import model
import utilities
from utilities import JsonBadRequest
import json

class Professors:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
        web.header('Content-type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        limit = utilities.get_limit(data, 100, 1000)
        offset = utilities.get_offset(data)
        type_ = ""
        reviews = False

        PROFESSOR_TYPES = ['professor', 'ta']
        if 'type' in data:
            if not data['type'] in PROFESSOR_TYPES:
                raise JsonBadRequest("type parameter must be either \"professor\" or \"ta\"")

            type_ = data['type']

        if 'reviews' in data:
            if not data['reviews'] in utilities.TRUE_FALSE:
                raise JsonBadRequest("reviews parameter must be either true or false")

            if data['reviews'] == 'true':
                reviews = True

        professors = list(model.get_professors(limit, offset, type_, reviews))

        return json.dumps(list(professors))
