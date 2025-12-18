# lectures/urls.py

from django.urls import path
from .views import (
    CourseListCreateView,
    LectureListCreateView,
    LectureDetailView,
    ResourceListView,
    CompleteQuizView,
)

urlpatterns = [
    path("courses/", CourseListCreateView.as_view()),
    path(
        "courses/<int:course_id>/lectures/",
        LectureListCreateView.as_view(),
    ),
    path(
        "lectures/<int:pk>/",
        LectureDetailView.as_view(),
    ),
    path(
        "resources/",
        ResourceListView.as_view(),
    ),
    path('quiz/<int:quiz_id>/complete/', CompleteQuizView.as_view(), name='quiz-complete'),
]
