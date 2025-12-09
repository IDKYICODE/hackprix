# lectures/admin.py

from django.contrib import admin
from .models import (
    Course,
    Lecture,
    Quiz,
    Question,
    Option,
    QuizSubmission,
    SubmissionAnswer,
    LectureAttendance,
    LearningResource,
)


# -------------------
# Inlines
# -------------------

class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 0
    fields = ("title", "visibility", "delivery_type", "scheduled_at", "is_active")
    show_change_link = True


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ("order", "text", "question_type", "marks")
    show_change_link = True


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    fields = ("text", "is_correct")


class SubmissionAnswerInline(admin.TabularInline):
    model = SubmissionAnswer
    extra = 0
    readonly_fields = (
        "question",
        "is_correct",
        "marks_obtained",
        "text_answer",
    )
    filter_horizontal = ("selected_options",)


# -------------------
# Admin classes
# -------------------

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "institution", "class_group", "is_active", "created_at")
    list_filter = ("is_active", "institution", "class_group")
    search_fields = ("title", "description", "teacher__username", "institution__name")
    inlines = [LectureInline]


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "teacher",
        "visibility",
        "delivery_type",
        "scheduled_at",
        "is_live",
        "is_active",
    )
    list_filter = (
        "visibility",
        "delivery_type",
        "is_live",
        "is_active",
        "institution",
        "class_group",
    )
    search_fields = ("title", "description", "course__title", "teacher__username")
    autocomplete_fields = ("course", "teacher", "institution", "class_group")


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "lecture", "is_active", "time_limit_seconds", "created_at")
    list_filter = ("is_active", "lecture__course",)
    search_fields = ("title", "lecture__title", "description")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_short", "quiz", "question_type", "marks", "order")
    list_filter = ("question_type", "quiz__lecture__course")
    search_fields = ("text", "quiz__title")
    inlines = [OptionInline]

    def text_short(self, obj):
        return (obj.text[:60] + "...") if len(obj.text) > 60 else obj.text
    text_short.short_description = "Question"


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "quiz",
        "student",
        "score",
        "max_score",
        "points_awarded",
        "created_at",
    )
    list_filter = ("quiz", "quiz__lecture__course", "student__institution")
    search_fields = ("student__username", "quiz__title")
    readonly_fields = (
        "quiz",
        "student",
        "started_at",
        "completed_at",
        "score",
        "max_score",
        "points_awarded",
        "points_tx_hash",
    )
    inlines = [SubmissionAnswerInline]

    def created_at(self, obj):
        return obj.started_at
    created_at.admin_order_field = "started_at"
    created_at.short_description = "Started at"


@admin.register(LectureAttendance)
class LectureAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "lecture",
        "student",
        "joined_at",
        "left_at",
        "total_duration_seconds",
        "points_awarded",
    )
    list_filter = ("lecture__course", "student__institution")
    search_fields = ("lecture__title", "student__username")
    readonly_fields = (
        "lecture",
        "student",
        "joined_at",
        "left_at",
        "total_duration_seconds",
        "points_awarded",
        "points_tx_hash",
    )


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "resource_type",
        "scope",
        "is_public",
        "created_at",
    )
    list_filter = ("resource_type", "is_public")
    search_fields = ("title", "description", "course__title", "lecture__title")
    autocomplete_fields = ("course", "lecture")

    def scope(self, obj):
        if obj.lecture:
            return f"Lecture: {obj.lecture.title}"
        if obj.course:
            return f"Course: {obj.course.title}"
        return "Global"

    scope.short_description = "Scope"
