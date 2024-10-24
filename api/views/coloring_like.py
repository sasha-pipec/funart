from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.like_coloring.create import ColoringLikeCreateService
from api.services.like_coloring.delete import ColoringLikeDeleteService


class ColoringLikeCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(ColoringLikeCreateService, {
            'id': kwargs['id'],
            'user': request.user
        })
        return Response({'coloring_id': kwargs['id']}, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        ServiceOutcome(ColoringLikeDeleteService, {
            'id': kwargs['id'],
            'user': request.user
        })
        return Response(status=status.HTTP_204_NO_CONTENT)
