from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from core.views import (
    CourseDetailView,
    CourseListView,
    CustomPasswordResetConfirmView,
    about,
    add_course,
    contact,
    course,
    delete_course,
    edit_course,
    edit_profile,
    home,
    lesson,
    signup,
    student,
    user_login,
    user_logout,
    verify_otp,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
    path("signup/", signup, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path(
        "verify-otp/<int:user_id>/",
        verify_otp,
        name="verify-otp",
    ),
    path("course/<str:name>/", course, name="course"),
    path("student/<int:id>/", student, name="student"),
    path(
        "course/<int:course_id>/lesson/<int:lesson_id>/",
        lesson,
        name="lesson",
    ),
    path(
        "courses/",
        CourseListView.as_view(),
        name="course-list",
    ),
    path(
        "courses/add/",
        add_course,
        name="course-add",
    ),
    path(
        "courses/<int:pk>/",
        CourseDetailView.as_view(),
        name="course-detail",
    ),
    path(
        "courses/<int:pk>/edit/",
        edit_course,
        name="course-edit",
    ),
    path(
        "courses/<int:pk>/delete/",
        delete_course,
        name="course-delete",
    ),
    path(
        "accounts/",
        include("allauth.urls"),
    ),
        path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="core/password_reset_form.html",
            email_template_name="core/password_reset_email.html",
            subject_template_name="core/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]