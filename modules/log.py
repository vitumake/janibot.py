#Error logs

#Ripped mostly from discord.py docs :)
#Im lazy

import logging
import logging.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

janiHandler = logging.handlers.RotatingFileHandler(
    filename='jani.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=2,  # Rotate through 5. files way too many wtf??
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
janiHandler.setFormatter(formatter)
logger.addHandler(janiHandler)