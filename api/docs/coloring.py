# -*- coding: utf8 -*-
from drf_yasg import openapi
from rest_framework import status

from api.docs.theme import THEME_ITEM
from api.docs.paginator import PAGINATOR_INFO

COLORING_ITEM = {
    "items": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(
                type=openapi.TYPE_INTEGER, example=1
            ),
            name=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
            image=openapi.Schema(type=openapi.TYPE_STRING, example="/uploads/colorings/index.jpg"),
            # created_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            # updated_at=openapi.Schema(type=openapi.TYPE_STRING, example="2023-02-25T15:15:51.217827+03:00"),
            # theme=openapi.Schema(
            #     type=openapi.TYPE_ARRAY,
            #     **THEME_ITEM
            # ),
        ),
    ),
}

COLORING_LIST_VIEW = {
    "operation_id": "Список раскрасок",
    "operation_description": """
        Выводит список всех раскрасок по определенной тематике 

        page - номер страницы (по умолчанию 1)
        per_page - сколько элементов на странице (по умолчанию 8)
        id - id желаемой тематики
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
                    colorings=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        **COLORING_ITEM
                    ),
                    theme=THEME_ITEM["items"],
                    page_data=openapi.Schema(type=openapi.TYPE_STRING, example='"[\"1\"]"'),
                    page_info=PAGINATOR_INFO,
                ),
            ),
        )
    },
}

COLORING_LIST_BY_SEARCH_VIEW = {
    "operation_id": "Список тематик по поиску",
    "operation_description": """
        Выводит список всех тематик по словам для поиска

        page - номер страницы (по умолчанию 1)
        per_page - сколько элементов на странице (по умолчанию 8)
        search - слова для поиска
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
        openapi.Parameter('search', openapi.IN_QUERY,
                          description="Слова для поиска раскрасок",
                          type=openapi.TYPE_STRING,
                          required=True),
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

COLORING_GET_VIEW = {
    "operation_id": "Получение раскраски",
    "operation_description": """
        Выводит раскраску по ее id

        id - id желаемой раскраски
    """,
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            COLORING_ITEM["items"]
        )
    },
}

COLORING_DOWNLOAD_VIEW = {
    "operation_id": "Скачивание раскраски",
    "operation_description": """
        Отдаёт jpeg файл по id раскраски
    """,
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
        )
    },
}

COLORING_CREATE_VIEW = {
    "operation_id": "Создание раскрасок",
    'manual_parameters': [
        openapi.Parameter('name', openapi.IN_QUERY,
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('image', openapi.IN_QUERY,
                          type=openapi.TYPE_FILE,
                          required=True),
    ],
}
