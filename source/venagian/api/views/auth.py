from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import HttpResponseBadRequest
from api.serializers import EmailAuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from api.tasks import password_recovery_email
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from drf_yasg import openapi  # type: ignore
from rest_framework.views import APIView

logger = logging.getLogger("django")

class GetToken(ObtainAuthToken):
    """
    Endpoint to get an Authorization token
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = EmailAuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "token": token.key,
                "role": user.get_user_type(user),
            }
        )


class PasswordRecoveryView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["email"],
        ),
        responses={
            200: "Password recovery email sent",
            400: "Invalid request",
        },
    )
    def post(self, request):
        email = request.data.get("email")
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "User does not exist"})

        password_recovery_email(user)

        return JsonResponse({"message": "Password recovery email sent"})
