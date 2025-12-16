# lectures/serializers.py

from rest_framework import serializers
from .models import (
    Course,
    Lecture,
    LearningResource,
)


# -------------------
# Course Serializer
# -------------------

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "teacher",
            "teacher_name",
            "institution",
            "class_group",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "teacher",
            "created_at",
        ]


# -------------------
# Lecture Serializer
# -------------------

class LectureSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True,
    )

    class Meta:
        model = Lecture
        fields = [
            "id",
            "course",
            "title",
            "description",
            "teacher",
            "teacher_name",
            "visibility",
            "delivery_type",
            "video_url",
            "resource_link",
            "vr_scene_id",
            "ar_experience_id",
            "scheduled_at",
            "duration_minutes",
            "is_live",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "teacher",
            "created_at",
        ]


# -------------------
# Learning Resource
# -------------------

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = [
            "id",
            "course",
            "lecture",
            "title",
            "description",
            "resource_type",
            "file",
            "external_url",
            "is_public",
            "order",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
