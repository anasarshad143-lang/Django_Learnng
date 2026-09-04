from django.contrib import admin
from django.urls import path,include



from core.views import (
    home,
    about,
    contact,
    course,
    student,
    lesson,
    CourseListView,
    CourseDetailView,
    add_course,
    signup,
    user_login,
    user_logout,
    edit_course,
    delete_course,
    edit_profile,
    
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
    name="course-delete"
    ),
   path('accounts/', include('allauth.urls'))
]