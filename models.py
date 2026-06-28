from django.db import models
from accounts.models import User
from doctors.models import AvailabilitySlot


class Booking(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'patient'}
    )

    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} booked {self.slot}"