import os
import sys
import pytest

from aiohttp import web

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from app import config
from app import create_app as create_main


@pytest.mark.asyncio
async def test_create_main():
    try:
        config.DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError:
        return

    app = await create_main()
    assert isinstance(app, web.Application)
