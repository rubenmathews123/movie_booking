from bookings.models import Seat, Movie

# Get all available movies
movies = list(Movie.objects.all())

# Get all seats
seats = Seat.objects.all()

if len(movies) < 2:
    print("⚠️ Not enough movies! Add more movies in the Django admin panel.")
else:
    # Rotate through movies and reassign seats
    for index, seat in enumerate(seats):
        seat.movie = movies[index % len(movies)]  # Assign seats in a round-robin way
        seat.save()

    print("✅ Seats reassigned successfully!")