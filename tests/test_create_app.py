import os
import sys
import pytest
import asyncpg

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)


from aiohttp import web
from app import create_app as create_main


@pytest.mark.asyncio
async def test_create_main():
    with pytest.raises(KeyError):
        app = await create_main()

    os.environ['DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/database'
    with pytest.raises(OSError):
        app = await create_main()
