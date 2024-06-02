from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.like_theme.create import LikeCreateService
from api.services.like_theme.delete import LikeDeleteService


class ThemeLikeCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(LikeCreateService, {
            'theme_id': kwargs['id'],
            'user': request.user
        })
        return Response({'theme_id': kwargs['id']}, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        ServiceOutcome(LikeDeleteService, {
            'id': kwargs['id'],
            'user': request.user
        })
        return Response(status=status.HTTP_204_NO_CONTENT)
