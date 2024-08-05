from drf_yasg import openapi
from rest_framework import status

BANNER_ITEM_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=dict(
        id=openapi.Schema(
            type=openapi.TYPE_NUMBER,
            example=1
        ),
        heading=openapi.Schema(
            type=openapi.TYPE_STRING,
            example='Heading of banner.',
        ),
        description=openapi.Schema(
            type=openapi.TYPE_STRING,
            example='Description of banner.',
        ),
        image=openapi.Schema(
            type=openapi.TYPE_STRING,
            example='/uploads/banners/image_banner',
        ),
    )
)

BANNER_LIST_VIEW = {
    "operation_id": "Список банеров.",
    "operation_description": """
        Выводит список всех банеров для главной страницы.
    """,
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            description="Success",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=BANNER_ITEM_SCHEMA
            )
        )
    },
}
