from django import forms
from .models import Course


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"