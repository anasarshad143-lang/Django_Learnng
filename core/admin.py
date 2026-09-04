from django.contrib import admin
from .models import Course, ContactMessage


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "price",
        "level",
        "is_published",
        "created_at",
    )

    list_filter = (
        "level",
        "is_published",
    )

    search_fields = (
        "title",
        "instructor",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)