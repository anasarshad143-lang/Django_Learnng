from django import forms
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]


    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(
            email=email
        ).exclude(
            id=self.instance.id
        ).exists():

            raise forms.ValidationError(
                "This email is already registered."
            )

        return email