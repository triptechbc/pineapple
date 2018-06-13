from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from university.laboratory.forms import SubmissionForm
from university.laboratory.models import Submission
from university.laboratory.serializers import SubmissionSerializer
from university.laboratory.utils import add_serializer_error_to_messages


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request, *args, **kwargs):
        response = super(SubmissionViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'submissions': response.data}, template_name='submission/list.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(SubmissionViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'submission': response.data}, template_name='submission/get.html')
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
        except Http404:
            pass
        return HttpResponseRedirect(reverse("submission-list"))

    def create(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('submission-detail', args=(instance.id, )))
        add_serializer_error_to_messages(request, serializer)
        return HttpResponseRedirect(reverse("submission-new"))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SubmissionSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('submission-detail', args=(instance.id, )))
        add_serializer_error_to_messages(request, serializer)
        return HttpResponseRedirect(reverse("submission-edit"))


class NewSubmission(APIView):
    """
    create a new submission
    """
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        """
        create new submission
        """
        form = SubmissionForm()
        return Response({'form': form}, template_name='submission/new.html')


class EditSubmission(APIView):
    """
    Edit a existing submission
    """
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request, pk=None):
        """
        edit a submission
        """
        try:
            instance = Submission.objects.get(id=pk)
        except Submission.DoesNotExist:
            messages.error(request, "Object not found")
            return HttpResponseRedirect(reverse("submission-list"))
        form = SubmissionForm(instance=instance)
        return Response({'form': form, 'submission': instance}, template_name='submission/edit.html')

