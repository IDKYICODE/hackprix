# lectures/models.py

from django.conf import settings
from django.db import models


# -------------------
# Course
# -------------------

class Course(models.Model):
    """
    A collection of lectures under a topic/subject.
    Can be public or tied to an institution/class.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    # Owner / teacher who created the course
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
        help_text="Primary teacher/creator of this course",
    )

    # Optional scoping
    institution = models.ForeignKey(
        "users.Institution",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="courses",
    )
    class_group = models.ForeignKey(
        "users.ClassGroup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="courses",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# -------------------
# Lecture
# -------------------

class Lecture(models.Model):
    """
    Single lecture/session. Can be video/VR/AR etc.
    """
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("institution", "Institution Only"),
        ("class", "Class Only"),
    ]

    DELIVERY_TYPE_CHOICES = [
        ("video", "Video"),
        ("vr", "VR"),
        ("ar", "AR"),
        ("hybrid", "Hybrid"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lectures",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lectures",
        help_text="Teacher delivering this lecture",
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    institution = models.ForeignKey(
        "users.Institution",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="lectures",
    )
    class_group = models.ForeignKey(
        "users.ClassGroup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="lectures",
    )

    delivery_type = models.CharField(
        max_length=20,
        choices=DELIVERY_TYPE_CHOICES,
        default="video",
    )

    # Links to actual content
    video_url = models.URLField(blank=True, null=True)
    resource_link = models.URLField(
        blank=True,
        null=True,
        help_text="Optional main link to PPT/notes/etc.",
    )

    # AR/VR metadata hooks
    vr_scene_id = models.URLField(
        
        blank=True,
        null=True,
        help_text="ID or slug used by the VR client to load this environment",
    )
    ar_experience_id = models.URLField(
       
        blank=True,
        null=True,
        help_text="ID for AR experience, if applicable",
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If this is a live/scheduled lecture",
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Approx duration, for UI only",
    )

    is_live = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"


# -------------------
# Quiz & Questions
# -------------------

class Quiz(models.Model):
    """
    Quiz attached to a specific lecture.
    """
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="quizzes",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    time_limit_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional time limit for quiz",
    )

    is_active = models.BooleanField(default=True)
    shuffle_questions = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.lecture.title})"


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("mcq_single", "MCQ - Single Correct"),
        ("mcq_multiple", "MCQ - Multiple Correct"),
        ("true_false", "True/False"),
        ("short_text", "Short Text"),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default="mcq_single",
    )
    marks = models.FloatField(default=1.0)

    order = models.PositiveIntegerField(
        default=0,
        help_text="Order of question within quiz",
    )

    def __str__(self):
        return f"Q{self.order} - {self.text[:40]}..."


class Option(models.Model):
    """
    Options for MCQ questions.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option for Q{self.question.id}: {self.text[:40]}..."


# -------------------
# Quiz Submissions
# -------------------

class QuizSubmission(models.Model):
    """
    One attempt by a student for a quiz.
    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_submissions",
    )

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0.0)
    max_score = models.FloatField(default=0.0)

    # Optional: link to blockchain tx for points awarded later
    points_awarded = models.PositiveIntegerField(default=0)
    points_tx_hash = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Blockchain transaction hash if points were awarded",
    )

    def __str__(self):
        return f"{self.student} - {self.quiz} ({self.score}/{self.max_score})"


class SubmissionAnswer(models.Model):
    """
    Stores answers per question for a submission.
    """
    submission = models.ForeignKey(
        QuizSubmission,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="submitted_answers",
    )

    # For MCQ
    selected_options = models.ManyToManyField(
        Option,
        blank=True,
        related_name="selected_in_answers",
    )

    # For text answers
    text_answer = models.TextField(blank=True)

    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0.0)

    def __str__(self):
        return f"Answer by {self.submission.student} for Q{self.question.id}"


# -------------------
# Attendance
# -------------------

class LectureAttendance(models.Model):
    """
    Basic attendance tracking for lectures.
    Can later be tied to points logic.
    """
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="attendances",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lecture_attendances",
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    total_duration_seconds = models.PositiveIntegerField(
        default=0,
        help_text="Approx duration the student was present in the session",
    )

    # Optional future: points linkage
    points_awarded = models.PositiveIntegerField(default=0)
    points_tx_hash = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = ("lecture", "student")

    def __str__(self):
        return f"{self.student} @ {self.lecture}"


# -------------------
# Learning Resources (Notes / PDFs / Ebooks / Links)
# -------------------

class LearningResource(models.Model):
    """
    Extra learning materials attached to a course or a specific lecture.
    e.g. notes, PDFs, ebooks, external links, etc.
    """
    RESOURCE_TYPE_CHOICES = [
        ("note", "Note"),
        ("pdf", "PDF"),
        ("ebook", "E-Book"),
        ("slides", "Slides"),
        ("assignment", "Assignment"),
        ("link", "External Link"),
        ("other", "Other"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="resources",
        null=True,
        blank=True,
        help_text="Resource at course level (available for all lectures)",
    )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="resources",
        null=True,
        blank=True,
        help_text="Resource specific to a particular lecture",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPE_CHOICES,
        default="pdf",
    )

    # Either file or external URL (or both)
    file = models.FileField(
        upload_to="learning_resources/",
        blank=True,
        null=True,
        help_text="Upload for PDFs, notes, ebooks, etc.",
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="Optional external link (Drive, website, etc.)",
    )

    is_public = models.BooleanField(
        default=True,
        help_text="If false, later you can restrict to enrolled students only.",
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="For ordering resources in UI",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        scope = "Course" if self.course and not self.lecture else "Lecture"
        return f"{scope} Resource: {self.title}"
