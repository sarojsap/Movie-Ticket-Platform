from rest_framework import viewsets
from .models import Movie, Theater, ShowTime
from .serializers import MovieSerializer, TheaterSerializer, ShowTimeSerializer

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