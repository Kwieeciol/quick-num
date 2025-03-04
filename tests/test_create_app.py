import os
import sys
import pytest
import asyncpg

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from app import config
from app import create_app as create_main

@pytest.mark.asyncio
async def test_create_main():
    # with pytest.raises(OSError):
    #     app = await create_main()

    try:
        config.DATABASE_URI = os.environ['DATABASE_URL']
    except KeyError:
        print("KEY ERROR DATABASE URL NOT FOUND")
    else:
        print('DATABASE URI:', os.environ['DATABASE_URL'])
        app = await create_main()
