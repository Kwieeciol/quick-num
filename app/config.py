from .utils import get_env

try:
    DATABASE_URI = get_env()['DATABASE_URI']
except KeyError:
    DATABASE_URI = ''
