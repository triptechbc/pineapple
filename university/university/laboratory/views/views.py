from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.views import APIView


class Index(APIView):
    """
    Landing Page
    """
    renderer_classes = (renderers.TemplateHTMLRenderer,)

    def get(self, request):
        """
        Landing page
        """
        return Response(template_name='base.html')
