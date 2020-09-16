from rest_framework import serializers
from .models import User
from ..schedule.models import Schedule
from ..schedule.serializers import ScheduleSerializer

from ..study.models import Study
from ..study.serializers import StudySerializer

from ..study_member.models import StudyMember



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'age', 'cellphone', 'gender', 'description', 'categories',
                  'kakao_profile_img','s3_profile_img','img_flag',]


class UserStudySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='study.study_id')
    title = serializers.ReadOnlyField(source='study.title')

    class Meta:
        model = StudyMember
        fields = ['id', 'title']


class UserDetailSerializer(serializers.ModelSerializer):
    '''
        UserList - patch
    '''
    study_list = UserStudySerializer(source='studymember_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'age', 'cellphone', 'gender', 'description', 'categories', 'study_list',
                  'kakao_profile_img','s3_profile_img','img_flag',]

        read_only_fields = ['user_id', 'email',]

class UserImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['s3_profile_img','img_flag']

class UserScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule

        fields = '__all__'

    #study_schedule = ScheduleSerializer(source='schedule_set', many=True)

    #class Meta:
    #    model = Study
    #    fields = ['study_schedule', ]



