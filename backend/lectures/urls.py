# lectures/urls.py

from django.urls import path
from .views import (
    CourseListCreateView,
    LectureListCreateView,
    LectureDetailView,
    ResourceListView,
    CompleteQuizView,
    RewardTimeView,
    CourseDetailByTitleView,  # New import
    LectureListByCourseTitleView, # New import
    ResourceListByCourseTitleView, # New import
)

urlpatterns = [
    path("courses/", CourseListCreateView.as_view()),
    path(
        "courses/<int:course_id>/lectures/",
        LectureListCreateView.as_view(),
    ),
    path(
        "courses/by_title/<str:title>/", # New URL pattern
        CourseDetailByTitleView.as_view(),
    ),
    path(
        "lectures/by_course_title/<str:course_title>/", # New URL pattern
        LectureListByCourseTitleView.as_view(),
    ),
    path(
        "lectures/<int:pk>/",
        LectureDetailView.as_view(),
    ),
    path(
        "resources/",
        ResourceListView.as_view(),
    ),
    path(
        "resources/by_course_title/<str:course_title>/", # New URL pattern
        ResourceListByCourseTitleView.as_view(),
    ),
    path('quiz/<int:quiz_id>/complete/', CompleteQuizView.as_view(), name='quiz-complete'),
    path('reward-time/', RewardTimeView.as_view(), name='reward-time'),
]