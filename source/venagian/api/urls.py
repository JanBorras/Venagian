from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"users", views.UserViewSet, basename="user")
router.register(r'csrf-token', views.CSRFTokenViewSet, basename='csrf-token')

urlpatterns = router.urls