from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.coloring import (
    COLORING_GET_VIEW,
)
from api.serializers.coloring.coloring_list_serializer import ColoringDetailSerializer
from api.services.coloring.coloring_get_service import ColoringGetService


class ColoringDetailView(APIView):

    @swagger_auto_schema(**COLORING_GET_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ColoringGetService, kwargs | {'user_id': request.user.id})
        return Response(ColoringDetailSerializer(outcome.result).data, status=status.HTTP_200_OK)
