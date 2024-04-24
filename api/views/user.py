from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.services.user.create import UserCreateServices


class CreateUserView(APIView):

    def post(self, request):
        try:
            ServiceOutcome(UserCreateServices, request.data)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


