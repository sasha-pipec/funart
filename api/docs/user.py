from drf_yasg import openapi
from rest_framework import status

USER_CREATE_VIEW = {
    "operation_id": "Регистрация пользователя",
    "operation_description": """
        Регистрация пользователя на сайте
    """,
    'manual_parameters': [
        openapi.Parameter('email', openapi.IN_QUERY,
                          description="Почта пользователя (body)",
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('username', openapi.IN_QUERY,
                          description="Логин пользователя (body)",
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('password', openapi.IN_QUERY,
                          description="Пароль пользователя (body)",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    "responses": {
        status.HTTP_201_CREATED: openapi.Response(
            "Success",
            examples={
                "application/json": {
                    "token": "test_token",
                }
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            "Success",
            examples={
                "application/json": {
                    "ValidationError": "A user with that email already exists",
                }
            },
        )
    },
}
