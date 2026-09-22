import secrets

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import EditProfileForm
from .models import EmailOTP, PasswordResetOTP
from .utils import send_brevo_email


# =========================================================
# SIGNUP
# =========================================================

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/signup.html",
                {"error": "Username already exists"}
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "accounts/signup.html",
                {"error": "Email already registered"}
            )

        # Create inactive user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        # Generate secure 6-digit OTP
        otp = str(
            secrets.randbelow(900000) + 100000
        )

        # Save OTP
        EmailOTP.objects.create(
            user=user,
            otp=otp
        )

        # Send verification OTP through Brevo
        response = send_brevo_email(
            to_email=email,
            subject="Verify Your E-Learning Account",
            html_content=f"""
                <h2>E-Learning Platform</h2>

                <p>Hello {username},</p>

                <p>Your verification code is:</p>

                <h1>{otp}</h1>

                <p>This code expires in 5 minutes.</p>
            """
        )

        # If Brevo failed
        if response.status_code != 201:

            user.delete()

            return render(
                request,
                "accounts/signup.html",
                {
                    "error":
                    "Could not send verification email. "
                    "Please try again."
                }
            )

        # Remember which account is being verified
        request.session["verification_user_id"] = user.id

        return redirect("verify_otp")

    return render(
        request,
        "accounts/signup.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.POST.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

        return render(
            request,
            "accounts/login.html",
            {
                "error":
                "Invalid username or password"
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(request)

    return redirect("home")


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):

    return render(
        request,
        "accounts/profile.html"
    )


# =========================================================
# SIGNUP OTP VERIFICATION
# =========================================================

def verify_otp(request):

    # Get user ID saved during signup
    user_id = request.session.get(
        "verification_user_id"
    )

    if not user_id:
        return redirect("signup")

    try:

        user = User.objects.get(
            id=user_id
        )

        otp_object = EmailOTP.objects.get(
            user=user
        )

    except (
        User.DoesNotExist,
        EmailOTP.DoesNotExist
    ):

        return redirect("signup")

    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp"
        )

        # Check if OTP expired
        if otp_object.is_expired():

            return render(
                request,
                "accounts/verify_otp.html",
                {
                    "error":
                    "OTP has expired. Please sign up again."
                }
            )

        # Check if OTP is correct
        if entered_otp == otp_object.otp:

            # Activate account
            user.is_active = True
            user.save()

            # Send welcome email
            send_brevo_email(
                to_email=user.email,
                subject="Welcome to E-Learning!",
                html_content=f"""
                    <h2>Welcome to E-Learning Platform</h2>

                    <p>Hello {user.username},</p>

                    <p>
                        Your email has been successfully
                        verified and your account is now active.
                    </p>

                    <p>
                        You can now log in and start
                        exploring our courses.
                    </p>

                    <p>
                        Best regards,<br>
                        E-Learning Team
                    </p>
                """
            )

            # Delete used OTP
            otp_object.delete()

            # Remove signup verification session
            request.session.pop(
                "verification_user_id",
                None
            )

            return redirect("login")

        # Wrong OTP
        return render(
            request,
            "accounts/verify_otp.html",
            {
                "error":
                "Invalid verification code."
            }
        )

    return render(
        request,
        "accounts/verify_otp.html"
    )


# =========================================================
# EDIT PROFILE
# =========================================================

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect("profile")

    else:

        form = EditProfileForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form": form
        }
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return render(
                request,
                "accounts/forgot_password.html",
                {
                    "error":
                    "No account was found with this email."
                }
            )

        # Generate new 6-digit OTP
        otp = str(
            secrets.randbelow(900000) + 100000
        )

        # Create OTP or replace previous OTP
        PasswordResetOTP.objects.update_or_create(
            user=user,
            defaults={
                "otp": otp,
                "created_at": timezone.now()
            }
        )

        # Send password reset OTP
        response = send_brevo_email(
            to_email=user.email,
            subject="Reset Your E-Learning Password",
            html_content=f"""
                <h2>E-Learning Platform</h2>

                <p>Hello {user.username},</p>

                <p>
                    Your password reset verification
                    code is:
                </p>

                <h1>{otp}</h1>

                <p>
                    This code expires in 5 minutes.
                </p>

                <p>
                    If you did not request a password
                    reset, you can ignore this email.
                </p>
            """
        )

        # If email could not be sent
        if response.status_code != 201:

            return render(
                request,
                "accounts/forgot_password.html",
                {
                    "error":
                    "Could not send the reset email. "
                    "Please try again."
                }
            )

        # Remember which user is resetting password
        request.session[
            "password_reset_user_id"
        ] = user.id

        # Remove any previous verified state
        request.session.pop(
            "password_reset_verified",
            None
        )

        return redirect(
            "verify_reset_otp"
        )

    return render(
        request,
        "accounts/forgot_password.html"
    )


# =========================================================
# VERIFY PASSWORD RESET OTP
# =========================================================

def verify_reset_otp(request):

    user_id = request.session.get(
        "password_reset_user_id"
    )

    if not user_id:
        return redirect("forgot_password")

    try:

        user = User.objects.get(
            id=user_id
        )

        otp_object = PasswordResetOTP.objects.get(
            user=user
        )

    except (
        User.DoesNotExist,
        PasswordResetOTP.DoesNotExist
    ):

        return redirect("forgot_password")

    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp"
        )

        # Check if OTP expired
        if otp_object.is_expired():

            return render(
                request,
                "accounts/verify_reset_otp.html",
                {
                    "error":
                    "OTP has expired. "
                    "Please request a new code."
                }
            )

        # Correct OTP
        if entered_otp == otp_object.otp:

            request.session[
                "password_reset_verified"
            ] = True

            return redirect(
                "reset_password"
            )

        # Wrong OTP
        return render(
            request,
            "accounts/verify_reset_otp.html",
            {
                "error":
                "Invalid verification code."
            }
        )

    return render(
        request,
        "accounts/verify_reset_otp.html"
    )


# =========================================================
# RESET PASSWORD
# =========================================================

def reset_password(request):

    user_id = request.session.get(
        "password_reset_user_id"
    )

    is_verified = request.session.get(
        "password_reset_verified"
    )

    # User must first verify OTP
    if not user_id or not is_verified:
        return redirect("forgot_password")

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        # Check both passwords match
        if password != confirm_password:

            return render(
                request,
                "accounts/reset_password.html",
                {
                    "error":
                    "Passwords do not match."
                }
            )

        # Proper Django password hashing
        user.set_password(password)

        user.save()

        # Delete password reset OTP
        PasswordResetOTP.objects.filter(
            user=user
        ).delete()

        # Clear password reset session
        request.session.pop(
            "password_reset_user_id",
            None
        )

        request.session.pop(
            "password_reset_verified",
            None
        )

        return redirect("login")

    return render(
        request,
        "accounts/reset_password.html"
    )