from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.coloring import (
    COLORING_LIST_VIEW, COLORING_CREATE_VIEW
)
from api.serializers.banner.list import BannerListSerializer
from api.serializers.coloring.list import ColoringListSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.banner.create import BannerCreateService
from api.services.banner.delete import BannerDeleteService
from api.services.banner.get import BannerDetailService
from api.services.banner.list import BannerListService
from api.services.coloring.create import ColoringCreateService
from api.services.coloring.list import ColoringListService


class BannerListCreateDeleteView(APIView):

    @swagger_auto_schema(**COLORING_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(BannerListService, {})
        return Response({
            "banners": BannerListSerializer(outcome.result.get('object_list'), many=True).data,
            'page_data': outcome.result.get('page_range'),
            'page_info': outcome.result.get('page_info'),
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(**COLORING_CREATE_VIEW, auto_schema=None)
    def post(self, request, *args, **kwargs):
        ServiceOutcome(
            BannerCreateService, request.data.dict(), {'image': request.data.get('image')}
        )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        ServiceOutcome(
            BannerDeleteService, {'id': request.data.get('id')}
        )
        return Response(status=status.HTTP_200_OK)


class BannerDetailView(APIView):

    @swagger_auto_schema(**COLORING_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(BannerDetailService, {'id': kwargs['id']})
        return Response({
            "banners": BannerListSerializer(outcome.result).data,

        }, status=status.HTTP_200_OK)
