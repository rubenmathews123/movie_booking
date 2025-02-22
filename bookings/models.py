from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seat_number', 'movie')  # Ensure unique seat per movie

    def __str__(self):
        return f"{self.movie.title} - Seat {self.seat_number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"