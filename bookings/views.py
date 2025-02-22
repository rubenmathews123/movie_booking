from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny

# -------------------------------
#  ✅ HOME & NAVIGATION
# -------------------------------
def home(request):
    """Render the home page with links to API & web views."""
    return render(request, 'bookings/home.html', {'show_api': False, 'show_web_pages': False})

def movie_list(request):
    """Render the movie list page."""
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

# -------------------------------
#  ✅ USER SIGNUP & AUTHENTICATION
# -------------------------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # ✅ Redirect to login after signup
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

# -------------------------------
#  ✅ SEAT BOOKING
# -------------------------------
def book_seat(request, movie_id):
    """Show available seats for a specific movie."""
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.filter(movie=movie, is_booked=False)  # ✅ Only show available seats
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

@login_required
def confirm_booking(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    # ✅ Fix: Check if seat is already booked BEFORE creating a booking
    if seat.is_booked:
        return JsonResponse(
            {"error": "This seat is already booked!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    movie = seat.movie  # Get the movie from the seat

    # ✅ Fix: Create the booking only if the seat is NOT booked
    booking = Booking.objects.create(user=request.user, movie=movie, seat=seat)

    # ✅ Fix: Mark seat as booked AFTER booking is created
    seat.is_booked = True
    seat.save()

    return JsonResponse(
        {"message": f"Successfully booked {seat.seat_number} for {movie.title}!"},
        status=status.HTTP_201_CREATED
    )
# -------------------------------
#  ✅ BOOKING HISTORY
# -------------------------------
@login_required
def booking_history(request):
    """Retrieve all bookings for the logged-in user."""
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

# -------------------------------
#  ✅ API VIEWSETS
# -------------------------------
class MovieViewSet(viewsets.ModelViewSet):
    """REST API for movies (CRUD operations)"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    """REST API for seats (availability & booking)"""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    """REST API for bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated] 