from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome
from api.services.token.delete import TokenDeleteServices
from api.services.token.get import TokenGetServices


class TokenGetDeleteView(APIView):
    def get(self, request):
        try:
            token = ServiceOutcome(TokenGetServices, request.data)
            return Response({'token': token.result.key}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        try:
            ServiceOutcome(TokenDeleteServices, {'user': request.user})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
