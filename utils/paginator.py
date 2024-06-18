import json
from typing import Any

from django.core.paginator import Paginator
from django.db.models import QuerySet

from conf.settings.rest_framework import REST_FRAMEWORK


def paginated_queryset(
        queryset: QuerySet,
        page: int = None,
        per_page: int = None
) -> dict[str, Any]:
    page = page or 1
    paginator = Paginator(
        queryset, per_page or REST_FRAMEWORK["PAGE_SIZE"],
    )
    page_info = {
        'has_previous': paginator.get_page(page).has_previous(),
        'has_next': paginator.get_page(page).has_next(),
        'num_page': json.dumps(page),
    }
    return {
        'page_info': page_info,
        'object_list': paginator.page(page).object_list,
        'page_range': ",".join([str(p) for p in paginator.page_range]),
    }
