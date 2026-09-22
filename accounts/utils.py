#we created this for brevo to work for otp verification email

import requests

from django.conf import settings


def send_brevo_email(to_email, subject, html_content):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    data = {
        "sender": {
            "name": "E-Learning Platform",
            "email": settings.BREVO_SENDER_EMAIL,
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=10
    )

    return response