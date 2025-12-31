from rest_framework import serializers
from .models import Movie, Theater, Hall, ShowTime, Seat, Booking, Ticket
from django.db import transaction

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

class BookingSerializer(serializers.ModelSerializer):
    # Input: We expect a list of seat IDs (UUIDs)
    seat_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'showtime', 'seat_ids', 'booked_at']
        read_only_fileds=['id', 'booked_at']

    def validate(self, data):
        # Check if seats are actually free.
        showtime = data['showtime']
        seat_ids = data['seat_ids']

        # 1. Check if seats belong to the correct hall
        # We query the Seat table to ensure these IDs exist in the showtime's hall
        seats = Seat.objects.filter(id__in=seat_ids, hall=showtime.hall)
        if len(seats) != len(seat_ids):
            raise serializers.ValidationError("Some seats are invalid or do not belong to this hall.")
        
        # 2. Check if seats are alrready booked for this showtime
        # We look at the ticket table
        taken_seats = Ticket.objects.filter(booking__showtime=showtime, seat__in=seat_ids)
        if taken_seats.exists():
            raise serializers.ValidationError("One or more selected seats are already booked.")
        
        # Save the seat objects in 'data' so we can use them in create() without querying again
        data['seats_objects'] = seats
        return data
    
    def create(self, validated_data):
        # The Atomic Transaction: Create Booking and Tickets together.
        seat_ids = validated_data.pop('seat_ids')   # Remove raw IDs
        seats = validated_data.pop('seats_objects') # Get the actual objects we found
        showtime = validated_data['showtime']
        user = self.context['request'].user # Get the logged-in user

        # START TRANSACTION
        with transaction.atomic():
            # 1. Create the Booking Parent Record
            booking = Booking.objects.create(user=user, showtime=showtime)

            # 2. CReate the individual Tickets
            tickets = [
                Ticket(booking=booking, seat=seat)
                for seat in seats
            ]
            Ticket.objects.bulk_create(tickets) # Efficiently insert all at once

        return booking
    
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'