from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now

from .models import AvailabilitySlot
from bookings.models import Booking
from django.contrib.auth import get_user_model

User = get_user_model()


# ==========================
# Doctor Dashboard
# ==========================

@login_required
def doctor_dashboard(request):

    slots = AvailabilitySlot.objects.filter(
        doctor=request.user
    ).order_by("date", "start_time")

    context = {
        "slots": slots,
        "available_count": slots.filter(is_booked=False).count(),
        "booked_count": slots.filter(is_booked=True).count(),
        "today_count": slots.filter(date=now().date()).count(),
    }

    return render(
        request,
        "doctor_dashboard.html",
        context
    )


# ==========================
# Add Slot
# ==========================

@login_required
def add_slot(request):

    if request.method == "POST":

        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        AvailabilitySlot.objects.create(
            doctor=request.user,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        messages.success(request, "Slot added successfully.")

        return redirect("doctor_dashboard")

    return render(request, "add_slot.html")


# ==========================
# Patient Dashboard
# ==========================

@login_required
def patient_dashboard(request):

    slots = AvailabilitySlot.objects.filter(
        is_booked=False
    ).select_related("doctor").order_by(
        "date",
        "start_time"
    )

    booking_count = Booking.objects.filter(
        patient=request.user
    ).count()

    upcoming_count = Booking.objects.filter(
        patient=request.user,
        slot__date__gte=now().date()
    ).count()

    doctor_count = User.objects.filter(
        role="doctor"
    ).count()

    context = {
        "slots": slots,
        "booking_count": booking_count,
        "upcoming_count": upcoming_count,
        "doctor_count": doctor_count,
    }

    return render(
        request,
        "patient_dashboard.html",
        context
    )