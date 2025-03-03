from aiohttp import web
from .api import create_app
from .utils import setup_logging


if __name__ == '__main__':
    with setup_logging():
        web.run_app(create_app(), port=8080)
