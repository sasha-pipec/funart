# -*- coding: utf8 -*-
from drf_yasg import openapi
from rest_framework import status

CATEGORY_ITEM = {
    "items": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(
                type=openapi.TYPE_INTEGER, example=1
            ),
            name=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            description=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            # created_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            # updated_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
        ),
    ),
}

CATEGORY_LIST_VIEW = {
    "operation_id": "Список категорий",
    "operation_description": """
        Выводит список всех категорий
    """,
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    categories=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **CATEGORY_ITEM
                    ),
                ),
            ),
        )
    },
}
