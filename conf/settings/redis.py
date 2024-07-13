# Redis config
from conf.settings.django import env

REDIS_HOST = env("REDIS_HOST", cast=str, default="127.0.0.1")
REDIS_PORT = env("REDIS_PORT", cast=str, default="6379")
CACHE_EXPIRE = env("CACHE_EXPIRE", cast=int)


REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": CACHE_EXPIRE,
    }
}
