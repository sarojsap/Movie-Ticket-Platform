from rest_framework import serializers
from .models import Movie, Theater, Hall, ShowTime, Seat, Booking, Ticket

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # Expose all fields

class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = '__all__'

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class ShowTimeSerializer(serializers.ModelSerializer):
    # When listing showtimes, the frontend needs the Movie details, not just the ID.
    # We can nest the MovieSerializer here just for reading.
    movie_details = MovieSerializer(source='movie', read_only=True)
    theater_name = serializers.CharField(source='hall.theater.name', read_only=True)
    hall_name = serializers.CharField(source='hall.name', read_only=True)

    class Meta:
        model = ShowTime
        fields = [
            'id', 'start_time', 'price',
            'movie', 'hall', # These are IDs(good for filtering/creating)
            'movie_details', 'theater_name', 'hall_name'    # These are readable details
        ]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'