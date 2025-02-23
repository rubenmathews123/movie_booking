from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from .views import (
    home, movie_list, book_seat, booking_history,
    MovieViewSet, SeatViewSet, BookingViewSet, confirm_booking, signup
)

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('movies/', movie_list, name='movie_list'),
    path('book-seat/<int:movie_id>/', book_seat, name='book_seat'),
    path('booking-history/', booking_history, name='booking_history'),
    path('confirm-booking/<int:seat_id>/', confirm_booking, name='confirm_booking'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/signup/', signup, name='signup'),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    path('api/', include(router.urls)),
]
