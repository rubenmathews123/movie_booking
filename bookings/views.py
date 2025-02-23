from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

def home(request):
    return render(request, 'bookings/home.html', {'show_api': False, 'show_web_pages': False})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

def book_seat(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = Seat.objects.filter(movie=movie).order_by(F('seat_number').asc())

    # Group seats into rows (10 seats per row)
    seat_rows = [seats[i:i + 10] for i in range(0, len(seats), 10)]

    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seat_rows': seat_rows})

@login_required
def confirm_booking(request, seat_id):
    seat = get_object_or_404(Seat, id=seat_id)

    if seat.is_booked:
        messages.error(request, "This seat is already booked!")
        return redirect('book_seat', movie_id=seat.movie.id)

    movie = seat.movie
    Booking.objects.create(user=request.user, movie=movie, seat=seat)

    seat.is_booked = True
    seat.save()

    messages.success(request, f"Successfully booked seat {seat.seat_number} for {movie.title}!")
    return redirect('booking_history')

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
