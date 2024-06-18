from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.category import CATEGORY_LIST_VIEW
from api.serializers.category.list import CategoryListSerializer
from api.services.category.list import CategoryListService


class CategoryListView(APIView):
    authentication_classes = []

    @swagger_auto_schema(**CATEGORY_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(CategoryListService, {})
        return Response({
            'categories': CategoryListSerializer(outcome.result, many=True).data
        }, status=status.HTTP_200_OK)
