# lectures/views.py

from rest_framework import generics, permissions
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

from .models import Course, Lecture, LearningResource
from .serializers import (
    CourseSerializer,
    LectureSerializer,
    LearningResourceSerializer,
)
from utils.blockchain import award_edutokens, ensure_checksum
from .models import Quiz, QuizSubmission


# -------------------
# Reward & XP
# -------------------

# lectures/views.py

# lectures/views.py

class RewardTimeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        duration_seconds = request.data.get("duration", 0)

        if not isinstance(duration_seconds, int) or duration_seconds <= 15:
            return Response({"message": "Session too short."}, status=200)

        reward_duration = min(duration_seconds, 3600)
        tokens_to_award = (reward_duration // 60) * 5
        xp_to_award = (reward_duration // 60) * 50

        # Save XP first so they always get it
        user.xp += xp_to_award
        user.save()

        tx_hash = None
        blockchain_error = None
        print('error before wallet')
        # Check for wallet first
        if not user.wallet_address:
            return Response({
                "message": f"Earned {xp_to_award} XP! Add a wallet to earn EDU tokens.",
                "xp_awarded": xp_to_award,
                "tokens_awarded": 0
            }, status=200)
        print('awarding tokens')
        if tokens_to_award > 0:
            tx_hash, blockchain_error = award_edutokens(ensure_checksum(user.wallet_address), tokens_to_award)
            
            if blockchain_error:
                # Still show XP but explain the token delay
                return Response({
                    "message": f"Earned {xp_to_award} XP! Token transfer pending: {blockchain_error}",
                    "xp_awarded": xp_to_award,
                    "tokens_awarded": 0,
                    "error": blockchain_error
                }, status=200)
        print("tokens awarded:", tokens_to_award, "tx_hash:", tx_hash )
        return Response({
            "message": f"You earned {xp_to_award} XP and {tokens_to_award} EDU!",
            "xp_awarded": xp_to_award,
            "tokens_awarded": tokens_to_award,
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
    



# -------------------
# AI Chatbot Integration
# -------------------

class ChatBotView(APIView):
    """
    POST /api/lectures/chat/
    Body: { "message": "What is photosynthesis?", "history": [...] }
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # 1. Initialize Client
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return Response({"error": "API Key not configured"}, status=500)
            
            client = genai.Client(api_key=api_key)

            # 2. Get Data
            user_message = request.data.get("message")
            history = request.data.get("history", [])

            if not user_message:
                return Response({"error": "No message provided"}, status=400)

            # 3. Format History for Gemini SDK
            chat_history = []
            for msg in history:
                role = "user" if msg.get('sender') == 'user' else "model"
                chat_history.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.get('text'))]
                ))

            # 4. Create Session and Generate Response
            chat = client.chats.create(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                    system_instruction=(
                        "You are a helpful and patient educational support bot. "
                        "Your goal is to help students understand concepts by guiding them "
                        "rather than just giving direct answers. Keep responses concise and encouraging."
                    )
                ),
                history=chat_history
            )

            response = chat.send_message(user_message)
            
            return Response({
                "response": response.text
            }, status=200)

        except Exception as e:
            print(f"Chatbot Error: {e}")
            return Response({"error": str(e)}, status=500)
        


import json
import random

class MultiPlayerQuizView(APIView):
    """
    Pure Django logic for a Multiplayer Quiz.
    Generates questions via Gemini and handles score submission.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, subject):
        """
        Endpoint to get 5 AI-generated questions for a subject.
        URL: /api/lectures/multi-quiz/generate/<subject>/
        """
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            client = genai.Client(api_key=api_key)

            # Strict prompt for structured data
            prompt = f"""Generate 5 multiple-choice quiz questions about {subject}.
            Format requirements:
            - Return ONLY a JSON list of objects.
            - Each object must have: "q" (string), "options" (list of 4 strings), "correct" (int 0-3).
            - Difficulty: Undergraduate level."""

            # Use response_mime_type to force Gemini to return pure JSON
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.8,
                )
            )

            # Because we used JSON mode, we don't need to strip ```json anymore
            questions = json.loads(response.text)

            # Shuffle options for variety while keeping track of the correct answer
            for item in questions:
                options = item['options']
                correct_answer = options[item['correct']]
                random.shuffle(options)
                item['correct'] = options.index(correct_answer)

            return Response({
                "subject": subject,
                "questions": questions
            }, status=200)

        except Exception as e:
            # This handles the 500 error and provides feedback
            print(f"Quiz Error: {str(e)}")
            return Response(
                {"error": "Failed to generate questions. Ensure your API key is valid."},
                status=500
            )

    def post(self, request):
        """
        Saves user score and awards XP.
        URL: /api/lectures/multi-quiz/submit-score/
        """
        user = request.user
        score = request.data.get("score", 0)
        
        # Logic to update user XP (from your existing user model)
        user.xp += int(score)
        user.save()

        return Response({
            "message": f"Quiz complete! {score} XP added to your profile.",
            "total_xp": user.xp
        }, status=200)