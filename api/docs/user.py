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
            "BAD_REQUEST",
            examples={
                "application/json": {
                    "ValidationError": "A user with that email already exists",
                }
            },
        )
    },
}

USER_GET_TOKEN_VIEW = {
    "operation_id": "Получение токена пользователя",
    'manual_parameters': [
        openapi.Parameter('email', openapi.IN_QUERY,
                          description="Почта пользователя (body)",
                          type=openapi.TYPE_STRING,
                          required=True),
        openapi.Parameter('password', openapi.IN_QUERY,
                          description="Пароль пользователя (body)",
                          type=openapi.TYPE_STRING,
                          required=True),
    ],
    "responses": {
        status.HTTP_201_CREATED: openapi.Response(
            "CREATED",
            examples={
                "application/json": {
                    "token": "test_token",
                }
            },
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            "BAD_REQUEST",
            examples={
                "application/json": {
                    "ValidationError": "Invalid password",
                }
            },
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            "NOT_FOUND",
            examples={
                "application/json": {
                    "ValidationError": "User not found",
                }
            },
        )
    },
}

USER_DELETE_TOKEN_VIEW = {
    "operation_id": "Удаление токена пользователя",
    "responses": {
        status.HTTP_204_NO_CONTENT: openapi.Response(
            "NO_CONTENT",
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            "UNAUTHORIZED",
            examples={
                "application/json": {
                    "NotAuthenticated": "Учетные данные не были предоставлены.",
                }
            },
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            "FORBIDDEN",
            examples={
                "application/json": {
                    "AuthenticationFailed": "Недопустимый токен.",
                }
            },
        )
    },
}
