from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.image.user_image import UserColoringSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.user_colorings.get import UserColoringGetService


class UserColoringDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserColoringGetService, {
            'user_coloring_id': kwargs['id'], 'user_id': request.user.id
        })
        return Response(
            {
                "user_coloring": UserColoringSerializer(outcome.result["object_list"]).data,
                "themes": ThemeListSerializer(outcome.result["themes"], many=True).data
            },
            status=status.HTTP_200_OK
        )
