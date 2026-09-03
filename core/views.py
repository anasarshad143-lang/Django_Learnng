from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course
from .forms import CourseForm


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    return render(request, "core/contact.html")


def course(request, name):
    return HttpResponse(f"You selected the {name} course.")


def student(request, id):
    return HttpResponse(f"You selected the {id} student.")


def lesson(request, course_id, lesson_id):
    return HttpResponse(
        f"Course: {course_id}, Lesson: {lesson_id}"
    )


class CourseListView(ListView):
    model = Course
    template_name = "core/course_list.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "core/course_detail.html"
    context_object_name = "course"


@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course-list")

    else:
        form = CourseForm()

    return render(request, "core/add_course.html", {"form": form})


@login_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect("course-detail", pk=course.pk)

    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "core/edit_course.html",
        {"form": form, "course": course}
    )


@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("course-list")

    return render(
        request,
        "core/delete_course.html",
        {"course": course}
    )


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            return render(
                request,
                "core/login.html",
                {"error": "Invalid username or password."}
            )

    return render(request, "core/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('edit_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})


