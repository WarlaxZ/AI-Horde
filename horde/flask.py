from flask import Flask
from flask_caching import Cache
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sqlalchemy import SQLAlchemy

from . import logger
from .redis_ctrl import is_redis_up

cache = None
HORDE = Flask(__name__)
db = SQLAlchemy()

HORDE.wsgi_app = ProxyFix(HORDE.wsgi_app, x_for=1)
HORDE.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///horde.db"
db.init_app(HORDE)

if is_redis_up():
    try:
        cache_config = {"CACHE_TYPE": "RedisCache", "CACHE_DEFAULT_TIMEOUT": 300}
        cache = Cache(config=cache_config)
        cache.init_app(HORDE)
        logger.init_ok("Flask Cache", status="Connected")
    except:
        pass

# Allow local workstation run
if cache == None:
    cache_config = {"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}
    cache = Cache(config=cache_config)
    cache.init_app(HORDE)
    logger.init_warn("Flask Cache", status="SimpleCache")
