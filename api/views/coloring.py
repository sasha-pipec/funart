from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.coloring import (COLORING_LIST_VIEW, COLORING_GET_VIEW,
                               COLORING_DOWNLOAD_VIEW, COLORING_CREATE_VIEW)
from api.serializers.coloring.list import ColoringListSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.coloring.all_list import ColoringAllListServices
from api.services.coloring.create import ColoringCreateServices
from api.services.coloring.download import ColoringDownloadService
from api.services.coloring.get import ColoringGetServices
from api.services.coloring.list import ColoringListServices


class ColoringAllDetailView(APIView):

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ColoringAllListServices, {'user_id': request.user.id})

        return Response(
            ColoringListSerializer(
                outcome.result,
                many=True
            ).data,
            status=status.HTTP_200_OK
        )


class ColoringListCreateView(APIView):

    @swagger_auto_schema(**COLORING_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ColoringListServices, request.GET.dict() | kwargs | {'user_id': request.user.id})

        return Response(
            {
                "colorings": ColoringListSerializer(outcome.result.get('object_list'), many=True).data,
                'page_data': outcome.result.get('page_range'),
                'page_info': outcome.result.get('page_info'),
                'theme': ThemeListSerializer(outcome.result.get('theme')).data,
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(**COLORING_CREATE_VIEW, auto_schema=None)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ColoringCreateServices, request.data.dict() | kwargs, {'image': request.data.get('image')}
        )
        return Response(
            status=status.HTTP_201_CREATED
        )


class ColoringDownloadView(APIView):

    @swagger_auto_schema(**COLORING_DOWNLOAD_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ColoringDownloadService, kwargs)
        return outcome.result


class ColoringDetailView(APIView):

    @swagger_auto_schema(**COLORING_GET_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ColoringGetServices, kwargs | {'user_id': request.user.id})
        return Response(
            ColoringListSerializer(
                outcome.result,
                many=False
            ).data,
            status=status.HTTP_200_OK
        )
