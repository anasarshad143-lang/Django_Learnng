from django.contrib import admin
from courses import views

from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses/", include("courses.urls")),
    path("user/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("enrollments/", include("enrollments.urls")),
    path(
    "payments/",
    include("payments.urls")
),
]