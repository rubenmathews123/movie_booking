from django.urls import path, include
from .views import (
    home, movie_list, book_seat, booking_history,
    MovieViewSet, SeatViewSet, BookingViewSet, confirm_booking
)
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import signup

# API Router for ViewSets
router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # Web Pages (HTML Views)
    path('', home, name='home'),  # Home page
    path('movies/', movie_list, name='movie_list'),  # Movie list page
    path('book-seat/<int:movie_id>/', book_seat, name='book_seat'), 
    #path('confirm-booking/<int:booking_id>/', confirm_booking, name='confirm_booking'), # Seat booking page
    path('booking-history/', booking_history, name='booking_history'),
    path('confirm-booking/<int:seat_id>/', confirm_booking, name='confirm_booking'),
      # Booking history page

    # API Endpoints (JSON)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # ✅ Login URL
    path('accounts/signup/', signup, name='signup'),
    path('api/', include(router.urls)),  # API routes
]