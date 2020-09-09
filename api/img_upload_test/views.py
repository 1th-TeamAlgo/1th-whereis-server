from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from ..user.models import User
from ..user.serializers import UserImageUploadSerializer

from .models import TestImage
from .serializers import TestImageSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError

from config.settings.secret import SECRET_KEY, ALGORITHM

import jwt

class TestImageList(APIView):
    @swagger_auto_schema(
        request_body=UserImageUploadSerializer,
        responses={201: UserImageUploadSerializer()},
        tags=['users/image'],
        operation_description=
        """
        현재 user의 프로필 사진을 바꿀때 사용하는 이미지 업로드용 api 이다
        
        현재 request 에는 image와 img_flag를 요청 받지만
        
        image만 보내주면 된다, img_flag는 서버 자체에서 이미지가 들어왔을때 처리를 해준다

        ---

        Header : x-jwt-token

        """,
    )
    def post(self,request):
        user_payload = self.jwt_get_payload(request)
        pk = user_payload['user_id']
        user = self.get_object(pk)
        print(request.data.update({'img_flag' : True}))
        print(request.data)
        serializer = UserImageUploadSerializer(user,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)


    def jwt_get_payload(self, request):
        try:
            user_jwt = request.META['HTTP_X_JWT_TOKEN']
            user_payload = jwt.decode(user_jwt, SECRET_KEY, algorithm=ALGORITHM)
            return user_payload

        except (KeyError, jwt.DecodeError):
            raise ParseError(detail="NO_JWT_TOKEN")