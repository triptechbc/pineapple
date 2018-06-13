from django.contrib import messages


def add_serializer_error_to_messages(request, serializer):
    for key, value in serializer.errors.items():
        for error in value:
            messages.error(request, error)