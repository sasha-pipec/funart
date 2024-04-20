from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.like.add import AddLikeServices
from api.services.like.delete import DelLikeServices


class DelLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(DelLikeServices, {
            'id': kwargs['id'],
            'user': request.user
        })
        return Response(status=status.HTTP_204_NO_CONTENT)
