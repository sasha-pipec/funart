from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.image.user_image import UserColoringSerializer
from api.services.image.user_image import UserColoringServices


class UserColoringDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserColoringServices,
                                 {'coloring_id': kwargs['id'],
                                  'user_id': request.user.id}
                                 )

        return Response(
            UserColoringSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )
