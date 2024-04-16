from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.token.get import GetTokenSerializers


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
