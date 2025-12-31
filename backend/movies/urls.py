from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, TheaterViewSet, ShowTimeViewSet, BookingViewSet, SeatViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'theaters', TheaterViewSet)
router.register(r'showtimes', ShowTimeViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'seats', SeatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
