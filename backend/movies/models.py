import uuid
from django.db import models
from django.conf import settings    #To refer to the User Model

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)
    # Note: For ImageField to work, we will need to configure Media Settings later

    def __str__(self):
        return self.title
    
class Theater(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"
    
class Hall(models.Model):
    # A specific room/screen inside a theater.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=100) # Example: "Screen 1 or IMAX Hall"
    
    def __str__(self):
        return f"{self.theater.name} - {self.name}"
    
class Seat(models.Model):
    # Individual Seats in a Hall
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)    # Example: "A", "B", "C"
    number = models.CharField(max_length=5) # Example: "1", "2", "3"

    # Constraint: We can't have two seats named "A1" in the same Hall
    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"{self.hall} - {self.row}{self.number}"
    
class ShowTime(models.Model):
    # When a movie is playing in a specific Hall.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} at {self.hall.name} ({self.start_time})"
    
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username}"
    
class Ticket(models.Model):
    # Represents one seat booked for on showtime.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    # Constraint: A seat cannot be booked twice for the same showtime.
    class Meta:
        unique_together = ('booking', 'seat')
        # Note: Ideally we need a constraint that checks (seat + showtime), 
        # but since 'seat' is linked to 'hall' and 'booking' linked to 'showtime',
        # we will enforce the "Seat Availability" logic in our Views/Serializers.

    def __str__(self):
        return f"Ticket for {self.seat} (Booking {self.booking.id})"