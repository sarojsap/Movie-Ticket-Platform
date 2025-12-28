from django.contrib import admin
from .models import Movie, Theater, Hall, Seat, ShowTime, Booking

admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(ShowTime)
admin.site.register(Booking)