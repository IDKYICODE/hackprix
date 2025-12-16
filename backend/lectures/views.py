# lectures/views.py

from rest_framework import generics, permissions
from django.db.models import Q

from .models import Course, Lecture, LearningResource
from .serializers import (
    CourseSerializer,
    LectureSerializer,
    LearningResourceSerializer,
)


# -------------------
# Courses
# -------------------

class CourseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/lectures/courses/
    POST /api/lectures/courses/
    """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        qs = Course.objects.filter(is_active=True)

        # Public courses
        public_qs = qs.filter(
            institution__isnull=True,
            class_group__isnull=True,
        )

        # Scoped courses
        scoped_qs = qs.filter(
            Q(institution=user.institution) |
            Q(class_group=user.class_group)
        )

        return (public_qs | scoped_qs).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "teacher":
            raise PermissionError("Only teachers can create courses")

        serializer.save(
            teacher=user,
            institution=user.institution,
            class_group=user.class_group,
        )


# -------------------
# Lectures under Course
# -------------------

class LectureListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/lectures/courses/<course_id>/lectures/
    POST /api/lectures/courses/<course_id>/lectures/
    """
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_id = self.kwargs["course_id"]

        qs = Lecture.objects.filter(
            course_id=course_id,
            is_active=True,
        )

        # Visibility filtering
        public_qs = qs.filter(visibility="public")
        institution_qs = qs.filter(
            visibility="institution",
            institution=user.institution,
        )
        class_qs = qs.filter(
            visibility="class",
            class_group=user.class_group,
        )

        return (public_qs | institution_qs | class_qs).distinct()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "teacher":
            raise PermissionError("Only teachers can create lectures")

        serializer.save(
            teacher=user,
            institution=user.institution,
            class_group=user.class_group,
            course_id=self.kwargs["course_id"],
        )


# -------------------
# Lecture Detail
# -------------------

class LectureDetailView(generics.RetrieveAPIView):
    """
    GET /api/lectures/lectures/<lecture_id>/
    """
    queryset = Lecture.objects.filter(is_active=True)
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------
# Learning Resources
# -------------------

class ResourceListView(generics.ListAPIView):
    """
    GET /api/lectures/resources/?course=<id>&lecture=<id>
    """
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = LearningResource.objects.filter(is_public=True)

        course_id = self.request.query_params.get("course")
        lecture_id = self.request.query_params.get("lecture")

        if course_id:
            qs = qs.filter(course_id=course_id)
        if lecture_id:
            qs = qs.filter(lecture_id=lecture_id)

        return qs
