"""
Logger configurations, this uses loguru to handle logs
Reference: https://github.com/Delgan/loguru
"""

import os
from loguru import logger as log

# configurations for log handling

# info log configurations
log.add(
    sink="logs/info.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="INFO"
)

# error logs
log.add(
    sink="logs/error.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="ERROR"
)

# debug logs
log.add(
    sink="logs/debug.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="DEBUG"
)

# warning logs
log.add(
    sink="logs/warn.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="WARNING"
)

# critical logs
log.add(
    sink="logs/critical.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="CRITICAL"
)

# trace logs
log.add(
    sink="logs/trace.log",
    backtrace=True
    if os.environ.get("FLASK_ENV", "development") == "development"
    else False,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    # format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True,
    rotation="20 MB",
    retention="5 days",
    compression="zip",
    level="TRACE"
)
