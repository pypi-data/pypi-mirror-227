# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

import sys
import os

from decouple import config

try:
    from dotenv import load_dotenv
    
    load_dotenv()
except ImportError:
    pass


class Var:
    # mandatory
    API_ID = config("API_ID", default=6, cast=int)
    API_HASH = config("API_HASH", default=None)
    SESSION = config("SESSION", default=None)
    REDIS_URI = config("REDIS_URL", default=None)
    REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
    MONGO_URI = config("MONGO_URI", default=None)
    BOT_TOKEN = config("BOT_TOKEN", default=None)
    LOG_CHANNEL = config("LOG_CHANNEL", default=123, cast=int)
    HEROKU_APP_NAME = config("HEROKU_APP_NAME", default=None)
    HEROKU_API = config("HEROKU_API", default=None)
    SUDO = config("SUDO", default=True, cast=bool)
    VC_SESSION = config("VC_SESSION", default=SESSION)
    ADDONS = config("ADDONS", default=False, cast=bool)
    INLINE_PIC = config("INLINE_PIC", default=False, cast=bool)
    VCBOT = config("VCBOT", default=True, cast=bool)
    DISABLE_PMDEL = config("DISABLE_PMDEL", default=True, cast=bool)
