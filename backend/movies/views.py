from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Theater, ShowTime, Booking, Seat
from .serializers import MovieSerializer, TheaterSerializer, ShowTimeSerializer, BookingSerializer, SeatSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

class ShowTimeViewSet(viewsets.ModelViewSet):
    queryset = ShowTime.objects.all().order_by('start_time')
    serializer_class = ShowTimeSerializer

    # We can filter ShowTimes
    def get_queryset(self):
        queryset = super().get_queryset()
        movie_id = self.request.query_params.get('movie_id')
        if movie_id:
            # get_queryset() let dynamically filter database results based on request parameters.
            queryset = queryset.filter(movie_id=movie_id)
        return queryset
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can access this

    def get_queryset(self):
        # Users should only see their own bookings, not everyone's
        return self.queryset.filter(user=self.request.user)
    
class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
    # Optional: Filter seats by hall_id. This will be very useful for the frontend.
    # Example: /api/seats/?hall_id=<uuid>
    def get_queryset(self):
        queryset = super().get_queryset()
        hall_id = self.request.query_params.get('hall_id')
        if hall_id:
            queryset = queryset.filter(hall_id=hall_id)
        return queryset