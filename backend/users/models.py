# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


# -------------------
# Institution Model
# -------------------

class Institution(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Short unique code used for joining, e.g. GRIET2025",
    )
    address = models.TextField(blank=True)

    # Additional fields
    logo = models.ImageField(
        upload_to="institution_logos/",
        blank=True,
        null=True,
    )
    banner_image = models.ImageField(
        upload_to="institution_banners/",
        blank=True,
        null=True,
    )
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    institution_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=[
            ("school", "School"),
            ("college", "College"),
            ("university", "University"),
            ("training", "Training Center"),
        ],
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# -------------------
# ClassGroup Model
# -------------------

class ClassGroup(models.Model):
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="class_groups",
    )
    name = models.CharField(
        max_length=100,
        help_text="Human readable name, e.g. 'CSE 3rd Year - A'",
    )
    grade = models.CharField(max_length=50, blank=True)

    # Additional fields
    section = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    academic_year = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="e.g. '2024-25'",
    )
    room_number = models.CharField(max_length=50, blank=True, null=True)
    avatar_theme = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    class_teacher_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("institution", "name")

    def __str__(self):
        return f"{self.institution.code} - {self.name}"


# -------------------
# User Model
# -------------------

class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("admin", "Admin"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
    )

    institution = models.ForeignKey(
        Institution,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    class_group = models.ForeignKey(
        ClassGroup,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="students",
    )

    # Blockchain
    wallet_address = models.CharField(
        max_length=42,
        blank=True,
        null=True,
        unique=True,
        help_text="Blockchain wallet address (0x...). Optional for now.",
    )

    # Additional profile info
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )
    gender = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
