from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.banner import (
    BANNER_LIST_VIEW,
)
from api.serializers.banner.list import BannerListSerializer
from api.services.banner.list import BannerListService


class BannerListView(APIView):

    @swagger_auto_schema(**BANNER_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(BannerListService, {})
        return Response(BannerListSerializer(outcome.result, many=True).data)
