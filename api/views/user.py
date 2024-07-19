from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.docs.user import USER_CREATE_VIEW
from api.serializers.user.list import UserMeSerializer
from api.serializers.user.token import TokenSerializer
from api.services.user.create import UserCreateService
from api.services.user.update_image import UserUpdateService


class CreateUpdateUserView(APIView):

    @swagger_auto_schema(**USER_CREATE_VIEW)
    def post(self, request):
        outcome = ServiceOutcome(UserCreateService, request.data, {'image': request.data.get('image')})
        return Response(TokenSerializer(outcome.result).data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        self.permission_classes = [IsAuthenticated, ]
        self.check_permissions(request)
        ServiceOutcome(UserUpdateService, {'user': request.user}, {'image': request.data.get('image')})
        return Response(status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema()
    def get(self, request):
        return Response(UserMeSerializer(request.user).data, status=status.HTTP_201_CREATED)
