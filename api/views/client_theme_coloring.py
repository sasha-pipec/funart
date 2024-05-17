from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.client.list_coloring import ClientColoringListSerializer
from api.serializers.client.list_themes import ClientThemeListSerializer
from api.services.client.list_coloring import ClientColoringListServices
from api.services.client.list_theme import ClientThemeListServices


class ClientThemeListGetView(APIView):
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ClientThemeListServices, kwargs)

        return Response(
            ClientColoringListSerializer(
                outcome.result['object_list'],
                many=True,
                context={'user': request.user}
            ).data,
            status=status.HTTP_200_OK
        )


class ClientColoringListGetView(APIView):
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(ClientColoringListServices, kwargs)

        return Response(
            ClientColoringListSerializer(
                outcome.result['object_list'],
                many=True,
                context={'user': request.user}
            ).data,
            status=status.HTTP_200_OK
        )
