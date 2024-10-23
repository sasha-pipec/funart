from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.serializers.coloring.coloring_list_serializer import ColoringListSerializer
from api.serializers.theme.list import ThemeListSerializer
from api.services.client.list_coloring import PersonalColoringListService
from api.services.client.list_theme import PersonalThemeListService


class PersonalThemeListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        outcome = ServiceOutcome(PersonalThemeListService, {'id': request.user.id})
        return Response({
            "themes": ThemeListSerializer(
                outcome.result.get('object_list'),
                many=True
            ).data,
            'page_data': outcome.result.get('page_range'),
            'page_info': outcome.result.get('page_info'),
        }, status=status.HTTP_200_OK)


class PersonalColoringListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        outcome = ServiceOutcome(PersonalColoringListService, {'id': request.user.id})
        return Response({
            "colorings": ColoringListSerializer(
                outcome.result.get('object_list'),
                many=True,
            ).data,
            'page_data': outcome.result.get('page_range'),
            'page_info': outcome.result.get('page_info'),
        }, status=status.HTTP_200_OK)
