"""university URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from university.laboratory.views.assignment import AssignmentViewSet, NewAssignment, EditAssignment, ViewSubmissions
from university.laboratory.views.submission import SubmissionViewSet, EditSubmission, NewSubmission
from university.laboratory.views.views import Index

assignment_destroy = AssignmentViewSet.as_view(
    {
    'post': 'destroy',
    }
)

assignment_update = AssignmentViewSet.as_view(
    {
    'post': 'update',
    }
)

submission_destroy = SubmissionViewSet.as_view(
    {
    'post': 'destroy',
    }
)

submission_update = SubmissionViewSet.as_view(
    {
    'post': 'update',
    }
)

router = DefaultRouter()
router.register("assignments", AssignmentViewSet)
router.register("submissions", SubmissionViewSet)

urlpatterns = format_suffix_patterns([
    url(r'^assignments/(?P<pk>[0-9]+)/delete$', assignment_destroy, name='assignment-delete'),
    url(r'^assignments/(?P<pk>[0-9]+)/update$', assignment_update, name='assignment-update'),
    url(r'^assignments/(?P<pk>[0-9]+)/edit$', EditAssignment().as_view(), name='assignment-edit'),
    url(r'^submissions/(?P<pk>[0-9]+)/delete$', submission_destroy, name='submission-delete'),
    url(r'^submissions/(?P<pk>[0-9]+)/update$', submission_update, name='submission-update'),
    url(r'^submissions/(?P<pk>[0-9]+)/edit$', EditSubmission().as_view(), name='submission-edit'),
    url(r'^assignments/(?P<pk>[0-9]+)/submissions$', ViewSubmissions().as_view(), name='assignment-submissions'),
])

urlpatterns += [
    path('assignments/new/', NewAssignment.as_view(), name='submission-new'),
    path('submissions/new/', NewSubmission.as_view(), name='submission-new'),
    path('', Index.as_view(), name='index'),
    ]

urlpatterns += router.urls

print(urlpatterns)