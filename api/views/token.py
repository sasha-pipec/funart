from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.token.get import GetTokenSerializers, DeleteTokenSerialuzers


class GetTockenView(APIView):
    def get(self, request):
        try:
            token_obj = GetTokenSerializers(data=request.data)
            token_obj.is_valid(raise_exception=True)
            return Response({
                'token': token_obj.validated_data['token']
            })
        except NotFound:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutTockenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = DeleteTokenSerialuzers(data={}, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            token = serializer.validated_data['obj_token']
            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
