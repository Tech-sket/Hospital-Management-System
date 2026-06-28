from django.db import models
from accounts.models import User


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'doctor'}
    )

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"Dr. {self.doctor.username} - {self.date} {self.start_time}-{self.end_time}"