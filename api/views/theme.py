from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.coloring import COLORING_LIST_BY_SEARCH_VIEW
from api.docs.theme import THEME_BY_CATEGORY_LIST_VIEW, THEME_LIST_VIEW, THEME_POPULAR_LIST_VIEW, THEME_CREATE_VIEW
from api.serializers.category.list import CategoryListSerializer
from api.services.coloring.search import SearchServices
from api.services.theme.category.list import ThemeListByCategoryService
from api.services.theme.create import ThemeCreateServices
from api.services.theme.list import ThemeListServices
from api.serializers.theme.list import ThemeListSerializer, ThemeListPopularSerializer
from api.services.theme.popular import ThemePopularListServices


class ThemeListCreateView(APIView):

    @swagger_auto_schema(**THEME_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ThemeListServices, request.GET.dict() | {'user_id': request.user.id})
        return Response(
            {
                "themes": ThemeListSerializer(
                    outcome.result.get('object_list'),
                    many=True,
                ).data,
                'page_data': outcome.result.get('page_range'),
                'page_info': outcome.result.get('page_info'),
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(**THEME_CREATE_VIEW, auto_schema=None)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ThemeCreateServices, request.data.dict(), {'image': request.data.get('image')})
        return Response(
            ThemeListSerializer(outcome.result, many=False).data,
            status=status.HTTP_201_CREATED
        )


class ThemePopularListView(APIView):

    @swagger_auto_schema(**THEME_POPULAR_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ThemePopularListServices, request.GET.dict() | {"user_id": request.user.id})
        return Response(
            {
                "themes": ThemeListPopularSerializer(
                    outcome.result,
                    many=True,
                    context={"user": request.user}
                ).data,
            },
            status=status.HTTP_200_OK
        )


class ThemeListByCategoryView(APIView):

    @swagger_auto_schema(**THEME_BY_CATEGORY_LIST_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ThemeListByCategoryService, request.GET.dict() | kwargs | {'user_id': request.user.id})
        return Response({
            'themes': ThemeListSerializer(outcome.result["object_list"], many=True).data,
            'category': CategoryListSerializer(outcome.result["category"]).data,
            'page_data': outcome.result.get('page_range'),
            'page_info': outcome.result.get('page_info'),
        }, status=status.HTTP_200_OK)


class ThemeListBySearchView(APIView):

    @swagger_auto_schema(**COLORING_LIST_BY_SEARCH_VIEW)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(SearchServices, request.GET.dict())
        return Response(
            {
                "themes": ThemeListSerializer(outcome.result.get('object_list'), many=True).data,
                'page_data': outcome.result.get('page_range'),
                'page_info': outcome.result.get('page_info'),
            },
            status=status.HTTP_200_OK
        )
