from django.urls import path, include
from wisestudy_app.category import views as category_views  # 카테고리
from wisestudy_app.user import views as user_views  # 유저
from wisestudy_app.study import views as study_views  # 스터디
from wisestudy_app.study_member import views as study_member_views  # 스터디원
from wisestudy_app.activity_picture import views as activity_picture_views  # 활동사진
from wisestudy_app.schedule import views as schedule_views  # 일정

urlpatterns = [
    # path('/category', include(category_patterns)),
    # path('/user', include(user_patterns)),
    # path('/user_category', include(user_category_patterns)),
    # path('/study', include(study_patterns)),
    # path('/study_member', include(study_member_patterns)),
    # path('/activity_picture', include(activity_picture_patterns)),
    # path('/schedule', include(schedule_patterns)),
    path('users', user_views.UserList.as_view()),
    path('users/<int:pk>', user_views.UserDetail.as_view()),
    path('categorys', category_views.CategoryList.as_view()),
    path('categorys/<int:pk>', category_views.CategoryDetail.as_view()),
]