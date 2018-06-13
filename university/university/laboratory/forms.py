from django.forms import ModelForm

from university.laboratory.models import Assignment, Submission


class AssignmentForm(ModelForm):
    """
    Assignment Form
    """
    class Meta:
        """
        AssignmentForm Meta
        """
        model = Assignment
        fields = '__all__'
        help_texts = {
            'date': 'Date format: YYYY-MM-DD',
        }


class SubmissionForm(ModelForm):
    """
    Submission Form
    """
    class Meta:
        """
        SubmissionForm Meta
        """
        model = Submission
        fields = ['student_name', 'date', 'raw_data_add', 'assignment']
        help_texts = {
            'date': 'Date format: YYYY-MM-DD',
        }
