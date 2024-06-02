from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.image.user_list_image import UserColoringsListSerializer
from api.services.image.user_list_image import UserColoringsListServices


class UserColoringsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        outcome = ServiceOutcome(UserColoringsListServices, {'user_id': request.user.id})

        return Response(
            {
                "colorings": UserColoringsListSerializer(
                    outcome.result.get('object_list'),
                    many=True,
                ).data,
                'page_data': outcome.result.get('page_range'),
                'page_info': outcome.result.get('page_info'),
            },
            status=status.HTTP_200_OK
        )
