from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, TheaterViewSet, ShowTimeViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'theaters', TheaterViewSet)
router.register(r'shotimes', ShowTimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
