"""
Serialiers
"""
from rest_framework import serializers

from university.laboratory.models import Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    """
    Assignment Serializer
    """

    submissions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        """
        Assignment Meta
        """
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Submission Serializer
    """

    class Meta:
        """
        Submission Meta
        """
        model = Submission
        fields = '__all__'

    def create(self, validated_data):
        obj = Submission.objects.create(**validated_data)
        obj.metadata1 = obj.assignment.metadata1
        obj.metadata2 = obj.assignment.metadata2
        obj.save()
        return obj


