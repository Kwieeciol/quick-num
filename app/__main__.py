import asyncio
import inspect

from . import api
from aiohttp import web
from .utils import setup_logging

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    

async def create_app() -> web.Application:
    app = web.Application()
    for ext, factory in [('/api', api.create_app)]:
        if inspect.iscoroutinefunction(factory):
            sub_app = await factory(app)
        else:
            sub_app = factory(app)  # type: ignore
        
        app.add_subapp(ext, sub_app)
        
    return app


if __name__ == '__main__':
    with setup_logging():
        web.run_app(create_app(), port=8080)
