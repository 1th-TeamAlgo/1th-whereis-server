from django.shortcuts import get_object_or_404
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class ScheduleList(APIView):
    @swagger_auto_schema(
        responses={200: ScheduleSerializer(many=True)},
        tags=['schedules'],
        operation_description=
        """
        스케줄 조회 API
    
        ---
        스케줄을 조회합니다.
        # 내용
            - schedule_id : 기본키(식별번호)
            - study_id : 스터디 기본키 참조(외래키)
            - datetime : 스터디 모임 시간
            - place : 스터디 모임 장소
            - address : 스터디 모임 주소
            - title : 스케줄 일정
            - description : 스케줄 간단 설명
        """,
    )
    def get(self, request):
        schedule = Schedule.objects.all()
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ScheduleSerializer,
        responses={200: ScheduleSerializer(many=True)},
        tags=['schedules'],
        operation_description=
        """
        스케줄 생성 API

        ---
        스케줄을 생성합니다.
        """,
    )
    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDetail(APIView):
    @swagger_auto_schema(
        responses={200: ScheduleSerializer(many=True)},
        tags=['schedules'],
        operation_description=
        """
        특정 id를 가진 스케줄 조회 API

        ---
        특정 id를 가진 스케줄을 조회합니다.
        # 내용
            - schedule_id : 기본키(식별번호)
            - study_id : 스터디 기본키 참조(외래키)
            - datetime : 스터디 모임 시간
            - place : 스터디 모임 장소
            - address : 스터디 모임 주소
            - title : 스케줄 일정
            - description : 스케줄 간단 설명
        """,
    )
    def get(self, request, pk):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # pk에 해당하는  POST 객체 반환
    def get_object(self, pk):
        return get_object_or_404(Schedule, pk=pk)

