from django.urls import path
from . import views

urlpatterns = [   # when someone visits " " we will show them CourseIst
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
]