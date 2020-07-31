from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class UserList(APIView):
    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        tags=['users'],
        operation_description=
        """
        회원 조회 API

        ---
        회원을 조회합니다.
        # 내용
            - user_id : 기본키(식별번호)
            - category_id : 카테고리 기본키 참조(외래키)
            - title : 스터디 그룹 이름
            - limit : 스터디 그룹 모집 최대인원
            - description : 스터디 그룹 간단소개
            - create_at : 스터디 그룹 생성날짜
            - update_at : 스터디 그룹 업데이트 날짜
        """,
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer(many=True)},
        tags=['users'],
        operation_description=
        """      
        회원 생성 API

        ---
        회원을 생성합니다.
        """,
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)

        data = self.metadata_class().determine_metadata(request, self)
        return Response({'a': 'a'}, status=status.HTTP_200_OK)


class UserDetail(APIView):
    @swagger_auto_schema(
        responses={200: UserSerializer(many=True)},
        tags=['users'],
        operation_description=
        """
        특정 id를 가진 회원 조회 API

        ---
        회원을 조회합니다.
        # 내용
            - user_id : 기본키(식별번호)
            - category_id : 카테고리 기본키 참조(외래키)
            - title : 스터디 그룹 이름
            - limit : 스터디 그룹 모집 최대인원
            - description : 스터디 그룹 간단소개
            - create_at : 스터디 그룹 생성날짜
            - update_at : 스터디 그룹 업데이트 날짜
        """,
    )
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # pk에 해당하는  POST 객체 반환
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer(many=True)},
        tags=['users'],
        operation_description=
        """
        특정 id를 가진 회원 수정 API

        ---
        회원을 수정합니다.
        """,
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserSerializer(many=True)},
        tags=['users'],
        operation_description=
        """
        특정 id를 가진 회원 삭제 API

        ---
        회원을 삭제합니다.
        """,
    )
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
