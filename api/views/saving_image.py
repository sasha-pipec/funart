import json

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.user_colorings.update_or_create import UserColoringCreateUpdateService


class SavingUserColoringView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ServiceOutcome(UserColoringCreateUpdateService,
                       {
                           'coloring_id': kwargs['coloring_id'],
                           'user_id': request.user.id,
                           'coloring_binary': request.data.get('coloring_json')
                       },
                       {'image': request.data['image']})
        return Response(status=status.HTTP_201_CREATED)
