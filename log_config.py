import logging
import sys

import asyncio
from asyncio_logger import AsyncLogger, StreamHandlerAsync, FileHandlerAsync


log_format = (
    '%(asctime)s - [%(levelname)s] -  %(name)s - '
    '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
)
logger = AsyncLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = StreamHandlerAsync(stream=sys.stdout)
stream_handler.setFormatter(logging.Formatter(log_format))

file_handler = FileHandlerAsync(
    f'{__file__}.log',
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding='UTF-8',
)
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
