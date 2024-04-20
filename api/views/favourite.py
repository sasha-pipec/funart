from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from api.services.favourite.add_del import FavouriteServices


class FavouriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(FavouriteServices, {
            'id': kwargs['id'],
            'user': request.user
        })

        return Response(status=status.HTTP_201_CREATED)
