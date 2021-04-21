import web
import model
import utilities
import json

class Search:
    def GET(self):
        model.insert_view(web.ctx.host + web.ctx.fullpath, web.ctx.status,
            web.ctx.ip, (web.ctx.env['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT'
                in web.ctx.env else None), "GET")
        web.header('Content-Type', 'application/json')
        web.header('Access-Control-Allow-Origin', '*')

        data = web.input()

        if "query" not in data:
            return utilities.api_error("parameters must include \"query\"")

        query = data.query
        results = model.search(query, 30)

        results_list = []
        for result in results:
            result = {
                "type": result.source,
                "name": result.name,
                "slug": result.slug,
            }
            results_list.append(result)

        return json.dumps(results_list)