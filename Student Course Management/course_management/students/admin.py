# Register your models here.
from django.contrib import admin
from .models import Student, Course, Enrollment, FileUpload

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course']
    search_fields = ['student__user__username', 'course__name']

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_by', 'course', 'timestamp']
    search_fields = ['file', 'uploaded_by__username', 'course__name']