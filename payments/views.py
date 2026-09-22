import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course
from enrollments.models import Enrollment
from .models import Payment


# Give Stripe our secret API key
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_checkout_session(request, course_id):

    # Get the course
    course = get_object_or_404(
        Course,
        id=course_id
    )

    # If user already owns the course,
    # don't allow them to buy it again
    if Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists():

        return redirect(
            "course_detail",
            course_id=course.id
        )

    # Stripe expects amount in the smallest currency unit.
    # PKR 2000 -> 200000
    amount_in_smallest_unit = int(
        course.price * 100
    )

    # Create Stripe Checkout Session
    checkout_session = stripe.checkout.Session.create(   #our django is asking Stripe Create a chekout session for this payment

        payment_method_types=[
            "card"
        ],

        mode="payment",

        customer_email=request.user.email,

        line_items=[
            {
                "price_data": {

                    # Pakistani Rupees
                    "currency": "pkr",

                    "product_data": {
                        "name": course.title,
                    },

                    "unit_amount": amount_in_smallest_unit,
                },

                "quantity": 1,
            }
        ],

        metadata={
            "user_id": str(request.user.id),
            "course_id": str(course.id),
        },

        success_url=(
            request.build_absolute_uri(
                "/payments/success/"
            )
            + "?session_id={CHECKOUT_SESSION_ID}"
        ),

        cancel_url=request.build_absolute_uri(
            f"/courses/course/{course.id}/"
        ),
    )

    # Save payment in our own database
    Payment.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        stripe_checkout_session_id=checkout_session.id,
        status="pending"
    )

    # Send user to Stripe
    return redirect(
        checkout_session.url
    )


@login_required
def payment_success(request):

    # Get Stripe Checkout Session ID from URL
    session_id = request.GET.get(
        "session_id"
    )

    if not session_id:
        return redirect("course_list")

    try:

        # Ask Stripe for the actual payment information
        checkout_session = (
            stripe.checkout.Session.retrieve(
                session_id
            )
        )

    except stripe.StripeError:

        return redirect("course_list")

    # Find the Payment that we created
    # before sending the user to Stripe
    payment = get_object_or_404(
        Payment,
        stripe_checkout_session_id=session_id,
        user=request.user
    )

    # IMPORTANT:
    # Only enroll if Stripe confirms payment
    if checkout_session.payment_status == "paid":

        # Mark our payment as paid
        payment.status = "paid"
        payment.save()

        # Create enrollment
        enrollment, created = (
            Enrollment.objects.get_or_create(
                user=request.user,
                course=payment.course
            )
        )

        print("PAYMENT STATUS:", checkout_session.payment_status)
        print("PAYMENT:", payment)
        print("ENROLLMENT:", enrollment)
        print("NEW ENROLLMENT CREATED:", created)

        return render(
            request,
            "payments/payment_success.html",
            {
                "payment": payment,
                "enrollment": enrollment,
            }
        )

    print(
        "PAYMENT NOT PAID:",
        checkout_session.payment_status
    )

    return redirect(
        "course_detail",
        course_id=payment.course.id
    )