from django.contrib import admin

# Register your models here.
from university.laboratory import models


@admin.register(models.Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Assignment Admin
    """
    list_display = ['title', 'date', 'text', 'metadata1',
                    'metadata2']
    search_fields = ['title', 'date']


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Submission Admin
    """
    list_display = ['student_name', 'date', 'raw_data_add', 'metadata1',
                    'metadata2', 'assignment']
    search_fields = ['student_name', 'date', 'assignment__title']
