from aiohttp import web

route = web.RouteTableDef()


@route.get('')
async def index(request: web.Request) -> web.Response:
    return web.json_response({'das': 123})


def create_app(main_app: web.Application) -> web.Application:
    app = web.Application()
    app.add_routes(route)
    return app
