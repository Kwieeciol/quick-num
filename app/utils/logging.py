from typing import Any

import logging
import contextlib

from logging.handlers import RotatingFileHandler

__all__ = ('setup_logging',)


class SupressFilter(logging.Filter):
    def filter(self, record):
        return not (record.name == 'aiohttp.access' and record.levelno == logging.INFO)


class ColorFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s',  # noqa: E501
            '%Y-%m-%d %H:%M:%S',
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


@contextlib.contextmanager
def setup_logging():
    log = logging.getLogger()

    try:
        max_bytes = 32 * 1024 * 1024  # 32 MiB

        log.setLevel(logging.INFO)

        logging.getLogger('aiohttp.access').addFilter(SupressFilter())

        handler = RotatingFileHandler(
            filename='server.log',
            encoding='utf-8',
            mode='w',
            maxBytes=max_bytes,
            backupCount=5
        )
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter(
            '[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{'
        )
        handler.setFormatter(fmt)
        log.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        log.addHandler(console_handler)

        yield
    finally:
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)
