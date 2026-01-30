# lectures/views.py

from rest_framework import generics, permissions
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta

from .models import Course, Lecture, LearningResource
from .serializers import (
    CourseSerializer,
    LectureSerializer,
    LearningResourceSerializer,
)
from .blockchain_utils import award_edutokens
from .models import Quiz, QuizSubmission


# -------------------
# Reward & XP
# -------------------

class RewardTimeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        duration_seconds = request.data.get("duration", 0)

        # 1. Basic Validation
        if not isinstance(duration_seconds, int) or duration_seconds <= 15:
            return Response({"message": "Session too short for rewards."}, status=200)

        # 2. Security Cap: Max 1 hour (3600s) to prevent "AFK" farming
        MAX_SECONDS = 3600
        reward_duration = min(duration_seconds, MAX_SECONDS)

        # 3. Reward Logic: 5 tokens per minute
        tokens_to_award = (reward_duration // 60) * 5
        xp_to_award = (reward_duration // 60) * 50 # 50 XP per minute

        user.xp += xp_to_award

        # 4. Streak Logic
        today = timezone.now().date()
        if user.last_login:
            last_login_date = user.last_login.date()
            if last_login_date == today - timedelta(days=1):
                user.streak += 1
            elif last_login_date < today - timedelta(days=1):
                user.streak = 1
        else:
            user.streak = 1

        user.last_login = timezone.now()
        user.save()

        # 5. Blockchain Award
        tx_hash = None
        error = None
        if user.wallet_address and tokens_to_award > 0:
            tx_hash, error = award_edutokens(user.wallet_address, tokens_to_award)
            if error:
                print(f"Blockchain Error: {error}")
                # Don't award tokens if there's an error
                tokens_to_award = 0

        message = "Reward processed!"
        if xp_to_award > 0 and tokens_to_award > 0:
            message = f"You earned {xp_to_award} XP and {tokens_to_award} EDU!"
        elif xp_awarded > 0: # Corrected from xp_awarded to xp_to_award
            message = f"You earned {xp_to_award} XP!"
        elif tokens_to_award > 0:
            message = f"You earned {tokens_to_award} EDU!"


        return Response({
            "message": message,
            "xp_awarded": xp_to_award,
            "tokens_awarded": tokens_to_award,
            "streak": user.streak,
            "tx_hash": tx_hash,
        }, status=200)


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


class CourseDetailByTitleView(generics.RetrieveAPIView):
    """
    GET /api/lectures/courses/by_title/<str:title>/
    Retrieves a single Course instance based on its title (case-insensitive).
    """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'title'
    lookup_url_kwarg = 'title'

    def get_queryset(self):
        return Course.objects.filter(is_active=True)

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field + '__iexact': self.kwargs[self.lookup_url_kwarg]}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        # Ensure the user has permission to view this course
        if not self.request.user.is_superuser and not (
            obj.institution == self.request.user.institution or
            obj.class_group == self.request.user.class_group or
            (obj.institution is None and obj.class_group is None) # Public course
        ):
            self.permission_denied(
                self.request,
                message="You do not have permission to access this course."
            )
        return obj


# -------------------
# Lectures under Course
# -------------------

class LectureListByCourseTitleView(generics.ListAPIView):
    """
    GET /api/lectures/lectures/by_course_title/<str:course_title>/
    Lists lectures for a specific course title (case-insensitive).
    Can be filtered by delivery_type (e.g., ?delivery_type=vr).
    """
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_title = self.kwargs["course_title"]

        qs = Lecture.objects.filter(
            course__title__iexact=course_title,
            is_active=True,
        )

        # Filter by delivery_type if provided
        delivery_type = self.request.query_params.get('delivery_type')
        if delivery_type:
            qs = qs.filter(delivery_type=delivery_type)

        # Visibility filtering (same as original LectureListCreateView)
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

class ResourceListByCourseTitleView(generics.ListAPIView):
    """
    GET /api/lectures/resources/by_course_title/<str:course_title>/
    Lists learning resources for a specific course title (case-insensitive).
    Can be filtered by resource_type (e.g., ?resource_type=pdf).
    """
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        course_title = self.kwargs["course_title"]

        qs = LearningResource.objects.filter(
            course__title__iexact=course_title,
        )

        # Filter by resource_type if provided
        resource_type = self.request.query_params.get('resource_type')
        if resource_type:
            qs = qs.filter(resource_type=resource_type)

        # Only show public resources for now, or resources associated with user's institution/class
        public_qs = qs.filter(is_public=True)
        scoped_qs = qs.filter(
            Q(course__institution=user.institution) |
            Q(course__class_group=user.class_group)
        )
        return (public_qs | scoped_qs).distinct()


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

class CompleteQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, quiz_id):
        user = request.user
        
        # 1. Demo Logic: Assume they passed and deserve 50 points
        reward_points = 50 
        
        # 2. Create DB record (using your existing model)
        submission = QuizSubmission.objects.create(
            quiz_id=quiz_id,
            student=user,
            score=100.0,
            max_score=100.0,
            points_awarded=reward_points
        )

        # 3. Blockchain Logic
        if user.wallet_address:
            tx_hash, error = award_edutokens(user.wallet_address, reward_points)
            
            if not error:
                # Update DB with the blockchain receipt (hash)
                submission.points_tx_hash = tx_hash
                submission.save()
                
                return Response({
                    "message": f"Successfully awarded {reward_points} EDU tokens!",
                    "tx_hash": tx_hash,
                    "db_id": submission.id
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": f"Blockchain failed: {error}"}, status=500)
        
        return Response({"message": "Quiz saved, but no wallet linked to award tokens."}, status=200)