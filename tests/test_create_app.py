import os
import sys
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)


from aiohttp import web
from app import create_app as create_main


@pytest.mark.asyncio
async def test_create_main():
    app = await create_main()
    assert isinstance(app, web.Application)
