from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.user import USER_GET_TOKEN_VIEW, USER_DELETE_TOKEN_VIEW
from api.serializers.user.token import TokenSerializer
from api.services.token.delete import TokenDeleteService
from api.services.token.get import TokenGetOrCreateService


class TokenGetDeleteView(APIView):
    @swagger_auto_schema(**USER_GET_TOKEN_VIEW)
    def post(self, request):
        outcome = ServiceOutcome(TokenGetOrCreateService, request.data)
        return Response(TokenSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**USER_DELETE_TOKEN_VIEW)
    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        ServiceOutcome(TokenDeleteService, {'user': request.user})
        return Response(status=status.HTTP_204_NO_CONTENT)
