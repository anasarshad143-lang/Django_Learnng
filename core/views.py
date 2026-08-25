

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render




def home(request):
    return render(request, 'core/home.html')

def contact(request):
    return HttpResponse("Contact us at anasarshad143@gmail.com")
def course(request, name):
    return HttpResponse(f"You selected the {name} course.")
def student(request,id):
    return HttpResponse(f"You selected the {id} student.")
def lesson(request, course_id, lesson_id):
    return HttpResponse(
        f"Course: {course_id}, Lesson: {lesson_id}"
    )
from django.shortcuts import render


def about(request):
    context = {
        "name": "Anas",
        "age": 21,
    }

    return render(request, "core/about.html", context)
