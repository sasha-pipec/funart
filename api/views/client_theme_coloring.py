from rest_framework import status
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from rest_framework.response import Response

from api.serializers.client.list_themes import ClientThemeListSerializer
from api.services.client.list import ClientThemeListServices
from models_app.models import Theme


class ClientThemeListGetView(APIView):
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ClientThemeListServices, kwargs)

        return Response(
            ClientThemeListSerializer(
                outcome.result['object_list'],
                many=True,
                context={'user': request.user}
            ).data,
            status=status.HTTP_200_OK
        )
