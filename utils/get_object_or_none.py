from django.core.exceptions import ObjectDoesNotExist


def get_object_or_none(model, pk):
    try:
        return model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None
