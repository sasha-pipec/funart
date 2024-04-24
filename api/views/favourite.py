from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from api.services.favourite.create import FavouriteCreateServices
from api.services.favourite.delete import FavouriteDeleteServices


class FavouriteCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        ServiceOutcome(FavouriteCreateServices, {
            'id': kwargs['id'],
            'user': request.user
        })

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        ServiceOutcome(FavouriteDeleteServices, {
            'id': kwargs['id'],
            'user': request.user
        })

        return Response(status=status.HTTP_204_NO_CONTENT)
