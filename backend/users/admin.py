# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Institution, ClassGroup


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "SmartEdu Details",
            {
                "fields": (
                    "role",
                    "institution",
                    "class_group",
                    "wallet_address",
                    "private_key",
                    "xp",
                    "streak",
                    "mobile_number",
                    "profile_image",
                    "gender",
                    "date_of_birth",
                    "bio",
                )
            },
        ),
    )

    list_display = (
        "username",
        "role",
        "institution",
        "class_group",
        "wallet_address",
        "private_key",
        "mobile_number",
        "is_staff",
        "is_active",
        "xp",
        "streak",
    )

    list_filter = (
        "role",
        "institution",
        "class_group",
        "gender",
        "is_staff",
        "is_active",
    )


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "institution_type",
        "contact_email",
        "created_at",
    )
    search_fields = ("name", "code")


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "institution",
        "academic_year",
        "section",
        "class_teacher_name",
        "created_at",
    )
    list_filter = ("institution", "academic_year")
    search_fields = ("name", "institution__name")
