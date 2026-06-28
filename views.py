from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from doctors.models import AvailabilitySlot
from google_calendar.utils import (
    create_calendar_event,
    refresh_token_if_expired,
)


# ---------------------------------------------------
# Check whether the logged-in user is a patient
# ---------------------------------------------------

def is_patient(user):
    return user.is_authenticated and user.role == "patient"


# ---------------------------------------------------
# Book Appointment
# ---------------------------------------------------

@login_required
@user_passes_test(is_patient)
def book_slot(request, slot_id):

    try:

        with transaction.atomic():

            # Lock the slot so two patients cannot book it simultaneously
            slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)

            if slot.is_booked:
                messages.error(
                    request,
                    "Sorry! This appointment has already been booked."
                )
                return redirect("patient_dashboard")

            slot.is_booked = True
            slot.save()

            booking = Booking.objects.create(
                patient=request.user,
                slot=slot
            )

        # ------------------------------------------------
        # Send Email Notification
        # ------------------------------------------------

        try:

            payload = {
                "type": "BOOKING_CONFIRMATION",
                "email": request.user.email,
                "name": request.user.username,
                "doctor_name": slot.doctor.username,
                "date": str(slot.date),
                "time": f"{slot.start_time} - {slot.end_time}"
            }

            requests.post(
                "http://localhost:3000/dev/email",
                json=payload,
                timeout=5
            )

        except Exception as e:
            print(f"Email service unavailable: {e}")

        # ------------------------------------------------
        # Create Google Calendar Events
        # ------------------------------------------------

        try:

            start_dt = datetime.combine(slot.date, slot.start_time)
            end_dt = datetime.combine(slot.date, slot.end_time)

            # Doctor Calendar

            if slot.doctor.google_token:

                token = refresh_token_if_expired(
                    slot.doctor.google_token
                )

                if token:
                    slot.doctor.google_token = token
                    slot.doctor.save()

                create_calendar_event(
                    token,
                    f"Appointment with {request.user.username}",
                    start_dt,
                    end_dt,
                    f"Patient Email: {request.user.email}"
                )

            # Patient Calendar

            if request.user.google_token:

                token = refresh_token_if_expired(
                    request.user.google_token
                )

                if token:
                    request.user.google_token = token
                    request.user.save()

                create_calendar_event(
                    token,
                    f"Appointment with Dr. {slot.doctor.username}",
                    start_dt,
                    end_dt,
                    f"Doctor: {slot.doctor.username}"
                )

        except Exception as e:
            print(f"Calendar Error: {e}")

        messages.success(
            request,
            "Appointment booked successfully!"
        )

        return redirect("patient_dashboard")

    except AvailabilitySlot.DoesNotExist:

        messages.error(request, "Appointment slot not found.")

    except IntegrityError:

        messages.error(
            request,
            "Someone booked this appointment just before you."
        )

    return redirect("patient_dashboard")


# ---------------------------------------------------
# My Bookings
# ---------------------------------------------------

@login_required
@user_passes_test(is_patient)
def my_bookings(request):

    bookings = Booking.objects.filter(
        patient=request.user
    ).select_related(
        "slot",
        "slot__doctor"
    ).order_by("-created_at")

    return render(
        request,
        "my_bookings.html",
        {
            "bookings": bookings
        }
    )