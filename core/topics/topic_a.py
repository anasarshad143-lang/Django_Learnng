#Views and Urls

#we must setup urls path like this for every view:

"""
from django.urls import path
from  appname. import views 

urlpatterns=[
path(" ", views.home)  #means if someone opens / this url go to home function in view

]
"""
#httpResponse
"""
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hi This is My E_learning website")

#this will send direct text/html to our websie but its not good approach
"""
#Render:
#this is hardcoded
"""
from django.shortcuts import render

def course_list(request):
    #context is the dictionary by which you pass dynamic data
    context={
        'course_name':'Python',
        'student_count':25
    }
"""

#now dynamic data directly from database

"""
from django.shortcuts import render
from .models import Course  # Assuming we have a Course model in database

def course_list_view(request):
    # Fetch ALL course objects directly from the database dynamically
    all_courses = Course.objects.all()
    
    # Put the database results into the context dictionary
    context = {
        'courses': all_courses  # Dynamic queryset!
    }
    
    return render(request, 'courses/course_list.html', context)

"""
#You must create an .html file inside your app's templates folder. This acts as the visual blueprint for your page