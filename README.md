# Django Learning – E-Learning Site

A Django-based E-Learning application built while learning Django fundamentals and following a structured Django syllabus.

The project is being developed step by step, with each feature used to practice the concepts covered during learning.

---

# Project Goal

The target application is an **E-Learning Site** where users will eventually be able to:

- View available courses
- View individual course details
- Add courses
- Edit existing courses
- Register and log in
- Manage their profile
- Use Django Forms
- Use authentication
- Work with custom templates
- Handle exceptions properly

---

# Technologies Used

- Python
- Django
- SQLite
- HTML
- Django Templates
- Django Forms
- Django ModelForms
- Django ORM

---

# Django Syllabus Progress

## A. Django URLs and Views Basics ✅

### 1. Django Project and App

Created a Django project and a `core` application.

Basic structure:

```text
e-learning/
│
├── manage.py
│
├── e_learning/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── core/
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── forms.py
    └── templates/
```

### 2. Django MVT Architecture

Learned the basic Django MVT flow:

```text
Browser
   ↓
URL
   ↓
View
   ↓
Model / Database
   ↓
View
   ↓
Template
   ↓
Browser
```

### 3. Function-Based Views

Created Function-Based Views such as:

```python
def home(request):
    return render(request, "core/home.html")
```

```python
def course_list(request):
    courses = Course.objects.all()

    context = {
        "courses": courses
    }

    return render(request, "core/course_list.html", context)
```

### 4. URL Routing

Learned how URLs are connected to views:

```python
path("", views.home),
path("courses/", views.course_list, name="course_list"),
```

### 5. Passing Data to Templates

Learned how to pass data from a view to a template using a context dictionary:

```python
context = {
    "courses": courses
}
```

And access the data in the template:

```html
{{ course.title }}
```

### 6. Dynamic URLs

Learned how to create URLs containing dynamic values:

```python
path(
    "courses/<int:course_id>/",
    views.course_detail,
    name="course_detail"
)
```

This allows URLs such as:

```text
/courses/1/
/courses/2/
/courses/5/
```

### 7. Django Template URL Tags

Learned how to generate URLs dynamically inside templates:

```html
<a href="{% url 'course_list' %}">
    View Courses
</a>
```

For dynamic URLs:

```html
<a href="{% url 'course_detail' course.id %}">
    View Details
</a>
```

---

## B. Advanced Django Views – Class-Based Views ⏳

**Status: Not covered yet**

Topics remaining:

- Class-Based Views
- Generic Views
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView

---

## C. Django Models, Migrations and ORM ✅

### 1. Django Models

Created a `Course` model to represent courses in the database.

Example:

```python
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
```

### 2. Model Properties

Learned that Django model fields represent database columns and model objects represent database records.

Examples:

```python
course.title
course.description
course.price
```

### 3. Migrations

Learned how Django converts model changes into database changes.

Basic flow:

```text
models.py
    ↓
makemigrations
    ↓
Migration file
    ↓
migrate
    ↓
Database
```

Commands:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 4. Django ORM

Learned how Django communicates with the database using the ORM instead of writing SQL directly.

Example:

```python
Course.objects.all()
```

This retrieves all courses.

### 5. Get a Specific Object

Learned:

```python
Course.objects.get(id=course_id)
```

to retrieve a specific course.

Also learned:

```python
get_object_or_404(Course, id=course_id)
```

which retrieves the object or returns a 404 response if it does not exist.

### 6. Find vs Get

Learned the difference between:

```python
Course.objects.get(...)
```

and:

```python
Course.objects.filter(...)
```

`get()` is used when expecting a single object.

`filter()` returns a QuerySet and can contain multiple objects.

---

## D. Django Forms and ModelForms ✅

### 1. Django Forms

Learned how Django Forms are used to collect and validate user input.

Basic process:

```text
User submits form
       ↓
request.POST
       ↓
Form
       ↓
is_valid()
       ↓
cleaned_data
```

### 2. GET and POST

Learned how to handle GET and POST requests.

Example:

```python
if request.method == "POST":
    form = CourseForm(request.POST)
else:
    form = CourseForm()
```

### 3. Form Validation

Learned how to validate submitted form data:

```python
if form.is_valid():
    ...
```

### 4. Cleaned Data

Learned how validated form data can be accessed:

```python
form.cleaned_data
```

Example:

```python
print(form.cleaned_data)
```

---

# ModelForms

### 1. Creating a ModelForm

Learned how a ModelForm connects directly to a Django model.

Example:

```python
class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"
```

### 2. How ModelForm Gets Model Fields

A ModelForm reads the model specified here:

```python
model = Course
```

Django then automatically creates form fields based on the fields defined in `models.py`.

For example:

```python
class Course(models.Model):
    title = models.CharField(...)
    description = models.TextField(...)
    price = models.IntegerField(...)
```

The ModelForm can automatically generate corresponding form fields.

### 3. `fields = "__all__"`

Learned that:

```python
fields = "__all__"
```

means:

> Include all editable fields from the model.

While:

```python
fields = ["title", "price"]
```

means:

> Only include these specific fields.

Important:

```python
fields = ["__all__"]  # Incorrect
```

because Django interprets `"__all__"` as a field name.

---

# Adding Courses

Implemented a complete Add Course feature.

Example view:

```python
def add_course(request):

    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("course_list")

    else:
        form = CourseForm()

    return render(
        request,
        "core/add_course.html",
        {"form": form}
    )
```

This feature taught:

- Creating a ModelForm
- Handling POST requests
- Validating forms
- Saving model data
- Redirecting after successful submission
- Rendering forms in templates

---

# Editing Existing Courses

Implemented editing of an existing course.

First, the existing course is retrieved:

```python
course = get_object_or_404(Course, id=course_id)
```

Then the existing object is passed into the ModelForm:

```python
form = CourseForm(instance=course)
```

When the form is submitted:

```python
form = CourseForm(
    request.POST,
    instance=course
)
```

After validation:

```python
form.save()
```

updates the existing database record instead of creating a new one.

---

# Add vs Edit

### Add Course

```python
form = CourseForm()
```

Then:

```python
form.save()
```

creates a new database record.

### Edit Course

```python
form = CourseForm(instance=course)
```

Then:

```python
form.save()
```

updates the existing record.

---

# Course Navigation

Added navigation links between pages using Django's template URL system.

Example:

```html
<a href="{% url 'course_list' %}">
    View Courses
</a>
```

Dynamic edit link:

```html
<a href="{% url 'edit_course' course.id %}">
    Edit Course
</a>
```

Current navigation flow:

```text
Home
 │
 ├── View Courses
 │      │
 │      ├── View Details
 │      │
 │      └── Edit Course
 │
 └── Add Course
```

---

# Current Project Features

At this stage, the application supports:

- Home page
- Course listing
- Course detail page
- Add Course
- Edit Course
- Django Models
- Database migrations
- Django ORM
- Django Forms
- ModelForms
- Form validation
- Dynamic URLs
- Template URL tags
- Basic navigation
- 404 handling using `get_object_or_404`

---

# Current URL Structure

```text
/                              → Home
/courses/                     → Course List
/courses/<course_id>/         → Course Detail
/courses/add/                 → Add Course
/edit-course/<course_id>/     → Edit Course
/admin/                       → Django Admin
```





