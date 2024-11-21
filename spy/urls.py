from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, TargetViewSet, MissionViewSet

router = DefaultRouter()
router.register(r"spycats", SpyCatViewSet)
router.register(r"targets", TargetViewSet)
router.register(r"missions", MissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
