from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from conf.settings.django import ENABLE_CASHING


def cash_off_on(CACHE_EXPIRE):
    def cash(fun):
        enable_caching = ENABLE_CASHING
        if enable_caching:
            @method_decorator(cache_page(CACHE_EXPIRE))
            def wrapper(request, *args, **kwargs):
                result = fun(request, *args, **kwargs)
                return result
        else:
            def wrapper(request, *args, **kwargs):
                result = fun(request, *args, **kwargs)
                return result
        return wrapper

    return cash
