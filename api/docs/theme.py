# -*- coding: utf8 -*-
from drf_yasg import openapi
from rest_framework import status

from api.docs.category import CATEGORY_ITEM
from api.docs.paginator import PAGINATOR_INFO

THEME_ITEM = {
    "items": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(
                type=openapi.TYPE_INTEGER, example=1
            ),
            name=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            description=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            image=openapi.Schema(type=openapi.TYPE_STRING, example="/uploads/themes/index.jpg"),
            # popular_image=openapi.Schema(type=openapi.TYPE_STRING, example="/uploads/themes/index.jpg"),
            # rating=openapi.Schema(type=openapi.TYPE_STRING, example="6"),
            created_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            updated_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            is_liked=openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            # category=openapi.Schema(
            #     type=openapi.TYPE_ARRAY,
            #     **CATEGORY_ITEM
            # ),
        ),
    ),
}


THEME_ITEM_POPULAR = {
    "items": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(
                type=openapi.TYPE_INTEGER, example=1
            ),
            name=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            popular_image=openapi.Schema(type=openapi.TYPE_STRING, example="/uploads/themes/index.jpg"),
            created_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            updated_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            is_liked=openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            # category=openapi.Schema(
            #     type=openapi.TYPE_ARRAY,
            #     **CATEGORY_ITEM
            # ),
        ),
    ),
}

THEME_BY_CATEGORY_LIST_VIEW = {
    "operation_id": "Список тематик по категории",
    "operation_description": """
        Выводит список всех тематик по определенной категориям
        
        page - номер страницы (по умолчанию 1)
        per_page - сколько элементов на странице (по умолчанию 8)
    """,
    'manual_parameters': [
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="Вы можете указать номер страницы, с которой хотите получить данные",
                          type=openapi.TYPE_NUMBER,
                          required=False),
        openapi.Parameter('per_page', openapi.IN_QUERY,
                          description="Вы можете выбрать количество тематик на странице",
                          type=openapi.TYPE_NUMBER,
                          required=False),
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    themes=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **THEME_ITEM
                    ),
                    category=CATEGORY_ITEM["items"],
                    page_data=openapi.Schema(type=openapi.TYPE_STRING, example='"[\"1\"]"'),
                    page_info=PAGINATOR_INFO,
                ),
            ),
        )
    },
}

THEME_LIST_VIEW = {
    "operation_id": "Список тематик",
    "operation_description": """
        Выводит список всех тематик

        page - номер страницы (по умолчанию 1)
        per_page - сколько элементов на странице (по умолчанию 8)
    """,
    'manual_parameters': [
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="Вы можете указать номер страницы, с которой хотите получить данные",
                          type=openapi.TYPE_NUMBER,
                          required=False),
        openapi.Parameter('per_page', openapi.IN_QUERY,
                          description="Вы можете выбрать количество тематик на странице",
                          type=openapi.TYPE_NUMBER,
                          required=False),
    ],
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    themes=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **THEME_ITEM
                    ),
                    page_data=openapi.Schema(type=openapi.TYPE_STRING, example='"[\"1\"]"'),
                    page_info=PAGINATOR_INFO,
                ),
            ),
        )
    },
}

THEME_POPULAR_LIST_VIEW = {
    "operation_id": "Список популярных тематик",
    "operation_description": """
        Выводит список популярных тематик
    """,
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    themes=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **THEME_ITEM_POPULAR
                    ),
                ),
            ),
        )
    },
}

THEME_CREATE_VIEW = {
    "operation_id": "Создание тематики",
    'manual_parameters': [
        openapi.Parameter('name', openapi.IN_QUERY,
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('description', openapi.IN_QUERY,
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('image', openapi.IN_QUERY,
                          type=openapi.TYPE_FILE,
                          required=True),
    ],
}
