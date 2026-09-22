from django.urls import path

from . import views


urlpatterns = [

    path(
        "checkout/<int:course_id>/",
        views.create_checkout_session,
        name="create_checkout_session"
    ),
    path(
    "success/",
    views.payment_success,
    name="payment_success"
   ),

]