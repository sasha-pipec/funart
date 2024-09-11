from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.image.user_image import UserColoringSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.user_colorings.delete import UserColoringDeleteService
from api.services.user_colorings.get import UserColoringGetService
from api.services.user_colorings.update import UserColoringUpdateService


class UserColoringDetailUpdateView(APIView):
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

    def patch(self, request, *args, **kwargs):
        data = request.data.dict() if request.data else request.data
        ServiceOutcome(UserColoringUpdateService, data | kwargs, request.FILES)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        ServiceOutcome(UserColoringDeleteService, kwargs)
        return Response(status=204)
