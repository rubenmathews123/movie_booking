from django.test import TestCase
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import date
from rest_framework.authtoken.models import Token

# ---------------------------
# 1️⃣ Unit Tests for Models
# ---------------------------
class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller",
            release_date=date(2010, 7, 16),
            duration=148,
            poster_url="https://example.com/poster.jpg"
        )

    def test_movie_creation(self):
        """Test if the movie is created successfully."""
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.description, "A mind-bending thriller")
        self.assertEqual(self.movie.release_date, date(2010, 7, 16))
        self.assertEqual(self.movie.duration, 148)

    def test_movie_string_representation(self):
        """Test if the __str__ method returns the movie title."""
        self.assertEqual(str(self.movie), "Inception")


class SeatModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Inception", release_date=date(2010, 7, 16), duration=148)
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False, movie=self.movie)

    def test_seat_creation(self):
        """Test if a seat is created properly."""
        self.assertEqual(self.seat.seat_number, "A1")
        self.assertFalse(self.seat.is_booked)
        self.assertEqual(self.seat.movie.title, "Inception")  # Ensure seat is linked to a movie


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.movie = Movie.objects.create(title="Inception", release_date=date(2010, 7, 16), duration=148)
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False, movie=self.movie)
        self.booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)

    def test_booking_creation(self):
        """Test if a booking is created properly."""
        self.assertEqual(self.booking.movie.title, "Inception")
        self.assertEqual(self.booking.seat.seat_number, "A1")
        self.assertEqual(self.booking.user.username, "testuser")

    def test_seat_is_marked_as_booked(self):
        """Test that a seat is marked as booked after booking."""
        
        # Ensure seat is booked
        self.seat.is_booked = True  # ✅ Explicitly mark as booked
        self.seat.save()  # ✅ Save to the database

        # Fetch updated seat from DB
        updated_seat = Seat.objects.get(id=self.seat.id)

        self.assertTrue(updated_seat.is_booked)  # ✅ Check if seat is marked booked

# ---------------------------
# 2️⃣ API Tests
# ---------------------------
class MovieAPITestCase(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Inception", release_date=date(2010, 7, 16), duration=148)

    def test_get_movies(self):
        """Test retrieving movie list API."""
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Inception")

    def test_create_movie(self):
        """Test creating a new movie."""
        response = self.client.post("/api/movies/", {
            "title": "Interstellar",
            "description": "A space exploration movie",
            "release_date": "2014-11-07",
            "duration": 169,
            "poster_url": "https://example.com/interstellar.jpg"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_movie_update(self):
        """Test updating a movie's title."""
        response = self.client.patch(f"/api/movies/{self.movie.id}/", {"title": "Inception Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Inception Updated")

    def test_movie_delete(self):
        """Test deleting a movie."""
        response = self.client.delete(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)


class SeatAPITestCase(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title="Inception", release_date=date(2010, 7, 16), duration=148)
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False, movie=self.movie)

    def test_get_seats(self):
        """Test retrieving seat list API."""
        response = self.client.get("/api/seats/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["seat_number"], "A1")

    def test_book_seat(self):
        """Test booking a seat."""
        response = self.client.patch(f"/api/seats/{self.seat.id}/", {"is_booked": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)


class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)  # ✅ Ensure authentication for API requests
        self.movie = Movie.objects.create(title="Inception", release_date=date(2010, 7, 16), duration=148)
        self.seat = Seat.objects.create(seat_number="A1", is_booked=False, movie=self.movie)

    def test_create_booking(self):
        """Test booking a seat API."""
        response = self.client.post("/api/bookings/", {
            "movie": self.movie.id,
            "seat": self.seat.id,
            "user": self.user.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_booking_list(self):
        """Test retrieving booking list API."""
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    