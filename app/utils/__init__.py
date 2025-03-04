import os

from .logging import *
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.cwd() / 'app' / '.env'


def get_env(path: os.PathLike | str = env_path) -> dict[str, str]:
    load_dotenv(path)
    return dict(os.environ)
