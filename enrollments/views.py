from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from .models import Enrollment


@login_required
def enroll_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return redirect(
        "course_detail",
        course_id=course.id
    )


@login_required
def my_courses(request):

    enrollments = Enrollment.objects.filter(
        user=request.user
    )

    return render(
        request,
        "enrollments/my_courses.html",
        {
            "enrollments": enrollments
        }
    )