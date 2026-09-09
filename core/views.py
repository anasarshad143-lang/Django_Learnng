import random
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import CourseForm, ProfileUpdateForm
from .models import ContactMessage, Course, EmailVerificationOTP


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)

        messages.success(request, "Your message has been sent successfully!")

        return redirect("contact")

    return render(request, "core/contact.html")


def course(request, name):
    return HttpResponse(f"You selected the {name} course.")


def student(request, id):
    return HttpResponse(f"You selected the {id} student.")


def lesson(request, course_id, lesson_id):
    return HttpResponse(f"Course: {course_id}, Lesson: {lesson_id}")


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
    if not request.user.is_staff:
        return redirect("course-list")

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
    if not request.user.is_staff:
        return redirect("course-list")

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)

        if form.is_valid():
            form.save()
            return redirect("course-detail", pk=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(
        request, "core/edit_course.html", {"form": form, "course": course}
    )


@login_required
def delete_course(request, pk):
    if not request.user.is_staff:
        return redirect("course-list")

    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        return redirect("course-list")

    return render(request, "core/delete_course.html", {"course": course})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(
                request,
                "core/signup.html",
                {"error": "Passwords do not match."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "core/signup.html",
                {"error": "Username already exists."},
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "core/signup.html",
                {"error": "Email already exists."},
            )

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )

        user.is_active = False
        user.save()

        otp = str(random.randint(100000, 999999))

        EmailVerificationOTP.objects.update_or_create(
            user=user, defaults={"otp": otp, "is_verified": False}
        )

        send_mail(
            "Email Verification - E-Learning",
            f"Your email verification OTP is: {otp}\n\n"
            "This OTP is valid for 10 minutes.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return redirect("verify-otp", user_id=user.id)

    return render(request, "core/signup.html")

def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    try:
        verification = EmailVerificationOTP.objects.get(user=user)
    except EmailVerificationOTP.DoesNotExist:
        return redirect("signup")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if verification.is_expired():
            return render(
                request,
                "core/verify_otp.html",
                {
                    "user_id": user_id,
                    "error": "OTP has expired. Please register again."
                }
            )

        if entered_otp == verification.otp:
            verification.is_verified = True
            verification.save()

            user.is_active = True
            user.save()

            messages.success(
                request,
                "Your email has been verified successfully. You can now log in."
            )

            return redirect("login")

        return render(
            request,
            "core/verify_otp.html",
            {
                "user_id": user_id,
                "error": "Invalid OTP. Please try again."
            }
        )

    return render(
        request,
        "core/verify_otp.html",
        {"user_id": user_id}
    )

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "core/login.html",
            {"error": "Invalid username or password."},
        )

    return render(request, "core/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            messages.success(
                request, "Your profile has been updated successfully!"
            )

            return redirect("edit_profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "core/edit_profile.html", {"form": form})