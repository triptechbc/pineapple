from django.db import models

# Models for university laboratory
from django.db.models import TextField, DateField, CharField
from djutil.models import TimeStampedModel


class Assignment(TimeStampedModel):
    """
    Assignment model
    """
    title = TextField()
    date = DateField()
    text = TextField()
    metadata1 = CharField(max_length=50, null=True, blank=True)
    metadata2 = CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('title', )

    def __str__(self):
        return self.title


class Submission(TimeStampedModel):
    """
    Student submission model
    """
    student_name = CharField(max_length=100)
    date = DateField()
    raw_data_add = CharField(max_length=100, null=True, blank=True)
    metadata1 = CharField(max_length=50, null=True, blank=True)
    metadata2 = CharField(max_length=50, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, related_name='submissions',
                                   on_delete=models.CASCADE, default=None)

    class Meta:
        unique_together = ('student_name', 'assignment')

    def __str__(self):
        return "%s - %s" % (self.assignment.title, self.student_name)
