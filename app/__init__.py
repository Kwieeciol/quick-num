import inspect

from . import api
from aiohttp import web

__all__ = ('create_app',)


async def create_app() -> web.Application:
    app = web.Application()
    for ext, factory in [('/api', api.create_app)]:
        if inspect.iscoroutinefunction(factory):
            sub_app = await factory(app)
        else:
            sub_app = factory(app)  # type: ignore
        
        app.add_subapp(ext, sub_app)
        
    return app
