# Create your models here.
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class EmailOTP(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_expired(self):
        return timezone.now() > (
            self.created_at + timedelta(minutes=5)
        )

    def __str__(self):
        return f"OTP for {self.user.username}"



class PasswordResetOTP(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def is_expired(self):

        return timezone.now() > (
            self.created_at
            + timedelta(minutes=5)
        )

    def __str__(self):

        return f"Password reset OTP for {self.user.username}"

    
