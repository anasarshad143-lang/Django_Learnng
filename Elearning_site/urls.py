from django.contrib import admin
from courses import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from accounts import views as account_views

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
    path(
    "api/token/",
    TokenObtainPairView.as_view(),
    name="token_obtain_pair",
    ),

    path(
    "api/token/refresh/",
    TokenRefreshView.as_view(),
    name="token_refresh",
    ),
    path(
    "api/profile/",
    account_views.api_profile,
    name="api_profile",
    ),
 
]