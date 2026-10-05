import os
from pathlib import Path

from dotenv import load_dotenv

from .logging import *

env_path = Path.cwd() / 'app' / '.env'


def get_env(path: os.PathLike | str = env_path) -> dict[str, str]:
    load_dotenv(path)
    return dict(os.environ)
