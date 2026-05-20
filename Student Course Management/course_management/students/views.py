from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import Student, Course, Enrollment, FileUpload
from .forms import FileUploadForm


# =========================
# HOME
# =========================
def home(request):
    return render(request, 'students/home.html')


# =========================
# REGISTER
# =========================
def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            # Automatically create student profile
            Student.objects.create(user=user)

            messages.success(request,
                             "Registration successful")

            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request,
                  'students/register.html',
                  {'form': form})


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(request,
                             "Login successful")

            return redirect('dashboard')

        else:

            messages.error(request,
                           "Invalid username or password")

    return render(request,
                  'students/login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):

    logout(request)

    return redirect('login')


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = Enrollment.objects.filter(
        student=student
    )

    uploaded_files = FileUpload.objects.filter(
        uploaded_by=request.user
    ).order_by('-id')[:5]

    return render(
        request,
        'students/dashboard.html',
        {
            'enrollments': enrollments,
            'recent_files': uploaded_files,
        }
    )


# =========================
# COURSE LIST + SEARCH
# =========================
@login_required
def course_list(request):

    query = request.GET.get('q')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            name__icontains=query
        )

    return render(
        request,
        'students/course_list.html',
        {
            'courses': courses
        }
    )


# =========================
# ENROLL IN COURSE
# =========================
@login_required
def enroll_in_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    student = get_object_or_404(
        Student,
        user=request.user
    )

    # Limit course enrollment
    if Enrollment.objects.filter(
            student=student
    ).count() >= 5:

        messages.error(
            request,
            "You cannot enroll in more than 5 courses."
        )

        return redirect('course_list')

    Enrollment.objects.get_or_create(
        student=student,
        course=course
    )

    messages.success(
        request,
        f"You enrolled in {course.name}"
    )

    return redirect('course_list')


# =========================
# FILE LIST
# =========================
@login_required
def file_list(request):

    files = FileUpload.objects.all()

    return render(
        request,
        'students/file_list.html',
        {'files': files}
    )


# =========================
# FILE UPLOAD
# =========================
@login_required
def upload_file(request):

    if request.method == 'POST':

        form = FileUploadForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            file = form.save(commit=False)

            file.uploaded_by = request.user

            file.save()

            messages.success(
                request,
                "File uploaded successfully"
            )

            return redirect('file_list')

    else:
        form = FileUploadForm()

    return render(
        request,
        'students/upload.html',
        {'form': form}
    )


# =========================
# DELETE FILE
# =========================
@login_required
def delete_file(request, file_id):

    file = get_object_or_404(
        FileUpload,
        id=file_id
    )

    # Only owner or admin can delete
    if (
        file.uploaded_by != request.user
        and
        not request.user.is_superuser
    ):

        messages.error(
            request,
            "You are not allowed to delete this file."
        )

        return redirect('file_list')

    file.delete()

    messages.success(
        request,
        "File deleted successfully."
    )

    return redirect('file_list')