import inspect
import asyncpg
import aiohttp

from aiohttp import web
from . import api, config

__all__ = ('create_app',)


async def create_app() -> web.Application:
    app = web.Application()
    pool = await asyncpg.create_pool(config.DATABASE_URI)
    session = aiohttp.ClientSession()

    async def on_cleanup(_):
        await pool.close()
        await session.close()

    app.on_cleanup.append(on_cleanup)

    for ext, factory in [('/api', api.create_app)]:
        if inspect.iscoroutinefunction(factory):
            sub_app = await factory(app, pool, session)
        else:
            sub_app = factory(app, pool, session)  # type: ignore

        app.add_subapp(ext, sub_app)

    return app
