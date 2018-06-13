from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, renderers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from university.laboratory.forms import AssignmentForm
from university.laboratory.models import Assignment
from university.laboratory.serializers import AssignmentSerializer
from university.laboratory.utils import add_serializer_error_to_messages


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request, *args, **kwargs):
        response = super(AssignmentViewSet, self).list(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'assignments': response.data}, template_name='assignment/list.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super(AssignmentViewSet, self).retrieve(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return Response({'assignment': response.data}, template_name='assignment/get.html')
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
        except Http404:
            pass
        return HttpResponseRedirect(reverse("assignment-list"))

    def create(self, request, *args, **kwargs):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('assignment-detail', args=(instance.id, )))
        add_serializer_error_to_messages(request, serializer)
        return HttpResponseRedirect(reverse("assignment-new"))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AssignmentSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()
            return HttpResponseRedirect(redirect_to=reverse('assignment-detail', args=(instance.id, )))
        add_serializer_error_to_messages(request, serializer)
        return HttpResponseRedirect(reverse("assignment-edit"))


class NewAssignment(APIView):
    """
    create a new assignment
    """
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request):
        """
        create new assignment
        """
        form = AssignmentForm()
        return Response({'form': form}, template_name='assignment/new.html')


class EditAssignment(APIView):
    """
    Edit a existing assignment
    """
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request, pk=None):
        """
        edit an assignment
        """
        try:
            instance = Assignment.objects.get(id=pk)
        except Assignment.DoesNotExist:
            messages.error(request, "Object not found")
            return HttpResponseRedirect(reverse("assignment-list"))
        form = AssignmentForm(instance=instance)
        return Response({'form': form, 'assignment': instance}, template_name='assignment/edit.html')


class ViewSubmissions(APIView):
    """
    View submissions of an assignment
    """
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def get(self, request, pk=None):
        """
        view submissions of an assignment
        """
        try:
            instance = Assignment.objects.get(id=pk)
        except Assignment.DoesNotExist:
            messages.error(request, "Object not found")
            return HttpResponseRedirect(reverse("assignment-list"))
        return Response({'submissions': instance.submissions.all(), 'assignment': instance}, template_name='assignment/submissions.html')

