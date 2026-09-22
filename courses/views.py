# Create your views here.
from django.shortcuts import render
from .models import Course
from enrollments.models import Enrollment
from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, "courses/home.html")


#this is our courselist VIEW
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course=course
        ).exists()

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "is_enrolled": is_enrolled,
        }
    )

def about(request):
    return render(request, "courses/about.html")


def contact(request):
    return render(request, "courses/contact.html")