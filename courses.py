import web
import model
import utilities
from utilities import JsonBadRequest
import json

class Courses:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status, web.ctx.ip, web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in web.ctx.env else None, "GET")
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        limit = utilities.get_limit(data, 100, 1000)
        offset = utilities.get_offset(data)
        department = ""
        reviews = False

        if 'department' in data:
            if len(data['department']) != 4:
                raise JsonBadRequest("department parameter must be 4 characters")

            department = data['department']

            if not model.department_has_course(department):
                raise JsonBadRequest("no courses found with that department")

        if 'reviews' in data:
            if not data['reviews'] in utilities.TRUE_FALSE:
                raise JsonBadRequest("reviews parameter must be either true or false")

            if data['reviews'] == 'true':
                reviews = True

        courses = model.get_courses(limit, offset, department, reviews)

        return json.dumps(list(courses))
