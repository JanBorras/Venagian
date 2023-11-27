import logging

from api.models import (
    User,
)
from api.serializers import (
    UserSerializer,
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth.hashers import make_password

logger = logging.getLogger("django")

class UserViewSet(viewsets.ModelViewSet):
    """
    User base class, all other user classes inherit from this class
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        return self.serializer_class

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        obj = super().get_object()

        # Check permissions for edit
        if self.request.method in ["PATCH"]:
            user = self.request.user

            # Only allow the user to edit/delete his own object
            if obj.id != user.id:
                return Response(
                    {"message": "You don't have permission to edit this"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return obj

    def perform_update(self, serializer):
        if "password" in serializer.validated_data:
            password = serializer.validated_data["password"]
            serializer.validated_data["password"] = make_password(
                password, salt=None, hasher="default"
            )
        serializer.save()