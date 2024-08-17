from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from conf.settings.redis import ENABLE_CASHING


def cache_off_on(CACHE_EXPIRE):
    def cache_decorator(fun):
        if ENABLE_CASHING:
            @method_decorator(cache_page(CACHE_EXPIRE))
            def wrapper(request, *args, **kwargs):
                result = fun(request, *args, **kwargs)
                return result
        else:
            def wrapper(request, *args, **kwargs):
                result = fun(request, *args, **kwargs)
                return result
        return wrapper

    return cache_decorator
