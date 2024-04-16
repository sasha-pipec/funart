from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.serializers.user.create import CreateUserSerializzer


class CreateUserView(APIView):
    def post(self, request):
        try:
            serializers = CreateUserSerializzer(data=request.data)
            serializers.is_valid(raise_exception=True)
            Token.objects.create(user=serializers.validated_data['user'])
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
