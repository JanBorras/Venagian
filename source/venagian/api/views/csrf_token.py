from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes

@authentication_classes([])
@permission_classes([])
class CSRFTokenViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # Retrieve the CSRF token from the request
        csrf_token = self.request.COOKIES.get('csrftoken', '')

        # Send the CSRF token as part of the response
        return Response({'csrfToken': csrf_token})