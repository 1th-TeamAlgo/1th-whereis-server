from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from ...user.models import User
from ...study.models import Study
from ..models import StudyMember

from ..serializers.study_add_study_member_sz import StudyAddStudyMemberSerializer

from ...study.serializers.member_of_study_sz import MemberOfStudySerializer

from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.cache import cache

from lib.user_data import jwt_get_payload

class StudyMemberConfirm(APIView):
    @swagger_auto_schema(
        tags=['studies'],
        operation_description=
        """
        스터디 가입 신청 넣은 인원 승인 api
        ---
            request_body
                - user_id : 스터디 가입 신청한 유저 id
        """,
    )
    ## study 가입 신청 멤버 승인
    def post(self, request, *args, **kwargs):
        study_id = self.kwargs['studies_id']
        str_study_id = self.str_study_id(study_id)

        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, pk=user_id)

        self.apply_member_delete_redis(str_study_id, user_id)

        if len(StudyMember.objects.filter(study_id=study_id, user_id=user_id)) > 0:
            return Response(data=["이미 들어있다"])

        study = get_object_or_404(Study, pk=study_id)
        study.study_members_count += 1
        study.save()

        study_member_data = {
            'study': study_id,
            'user': user_id,
            'is_manager': False,
        }

        study_member_serializer = StudyAddStudyMemberSerializer(data=study_member_data)

        if study_member_serializer.is_valid():
            study_member_serializer.save()

        study_members = get_object_or_404(Study, pk=study_id)
        study_members_serializer = MemberOfStudySerializer(study_members)
        return Response(study_members_serializer.data)

    @swagger_auto_schema(
        tags=['studies'],
        operation_description=
        """
        스터디 가입 신청 인원 거절 
        ---
            request_body
                - user_id : 스터디 가입 신청한 유저 id
        """,
    )
    ## study 가입 신청 멤버 반려
    def delete(self, request, *args, **kwargs):
        user_payload = jwt_get_payload(request)
        study_id = self.kwargs['studies_id']

        if self.user_is_manager(user_id=user_payload['user_id'], studies_id=study_id):
            str_study_id = self.str_study_id(study_id)

            user_id = request.POST.get('user_id')

            study_apply_dict = self.apply_member_delete_redis(str_study_id, user_id)

            return Response(data=study_apply_dict)

        else:
            return Response(data=['관리자가 아닙니다'])

    ## 가입 승인 또는 반려 된 인원 redis에서 제거
    def apply_member_delete_redis(self, study_id, user_id):
        study_apply_dict = cache.get(study_id)

        if int(user_id) in study_apply_dict.keys():
            study_apply_dict.pop(int(user_id))
            cache.set(study_id, study_apply_dict)
            print(study_apply_dict)

        return study_apply_dict

    def str_study_id(self, study_id):
        return 'study:' + str(study_id)

    def user_is_manager(self, studies_id, user_id):
        is_manager = get_object_or_404(StudyMember, study=studies_id, user=user_id)
        if hasattr(is_manager, 'is_manager') is not None and getattr(is_manager, 'is_manager') is True:
            return True
        else:
            return False
