from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.image.user_image import UserColoringSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.user_colorings.get import UserColoringGetService
from api.services.user_colorings.update import UserColoringUpdateService
from models_app.models import UserColoring


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
        ServiceOutcome(UserColoringUpdateService, {
            'user_coloring_id': kwargs['id'], 'user_id': request.user.id,
            'coloring_json': request.data.get('coloring_json'),
        },
                       {'image': request.data.get('image')})
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        delete_user_coloring = UserColoring.objects.get(
            id=kwargs['id']
        )
        delete_user_coloring.delete()
        return Response(status=204)
