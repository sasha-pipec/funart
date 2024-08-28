from django.core.exceptions import ObjectDoesNotExist


def get_or_none(model_class, **kwargs):
    try:
        return model_class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
