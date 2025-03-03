import os
import re
import logging
import inspect
import importlib

from aiohttp import web

log = logging.getLogger(__name__)
__all__ = ('create_app',)


async def create_app(main_app: web.Application) -> web.Application:
    app = web.Application()
    pattern = re.compile(r'v\d+')
    path = os.path.dirname(os.path.realpath(__file__))

    for f in os.listdir(path):
        if not pattern.match(f):
            continue
        
        route = f'/{f}'
        module = importlib.import_module(f'{__name__}.{f}')
        if not hasattr(module, 'create_app'):
            logging.error(
                f'Could not add sub app {route!r} (no entry point found)'
            )
            continue
        
        if inspect.iscoroutinefunction(module.create_app):
            sub_app = await module.create_app(app)
        else:
            sub_app = module.create_app(app)
        
        app.add_subapp(route, sub_app)
        logging.info(f'Successfully added sub app {route!r}')
    
    return app
