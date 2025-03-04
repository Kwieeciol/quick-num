import os
import re
import logging
import asyncpg
import inspect
import importlib

from aiohttp import web
from aiohttp import ClientSession

__all__ = ('create_app',)

log = logging.getLogger(__name__)
pg_pool: web.AppKey[asyncpg.Pool] = web.AppKey('pg_pool', asyncpg.Pool)
session: web.AppKey[ClientSession] = web.AppKey('session', ClientSession)


async def create_app(
    main_app: web.Application, pool: asyncpg.Pool, cs: ClientSession
) -> web.Application:
    app = web.Application()
    app[pg_pool] = pool
    app[session] = cs

    pattern = re.compile(r'v\d+')
    path = os.path.dirname(os.path.realpath(__file__))

    for f in os.listdir(path):
        if not pattern.match(f):
            continue

        route = f'/{f}'
        module = importlib.import_module(f'{__name__}.{f}')
        if not hasattr(module, 'create_app'):  # pragma: no cover
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
