from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.like_theme.create import LikeCreateServices
from api.services.like_theme.delete import LikeDeleteServices


class ThemeLikeCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(LikeCreateServices, {
            'theme_id': kwargs['id'],
            'user': request.user
        })
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        ServiceOutcome(LikeDeleteServices, {
            'id': kwargs['id'],
            'user': request.user
        })
        return Response(status=status.HTTP_204_NO_CONTENT)
