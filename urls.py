from django.urls import path
from . import views

urlpatterns = [
    path(
        "book-slot/<int:slot_id>/",
        views.book_slot,
        name="book_slot",
    ),

    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings",
    ),
]