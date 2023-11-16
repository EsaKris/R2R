from django.db import models
from homepage.models import Attendees
from django.utils import timezone


class CreateAttendance(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self) -> str:
        return f'{self.title}'

class Attendance(models.Model):
    attendance = models.ForeignKey(CreateAttendance, on_delete=models.CASCADE,related_name="list")
    attendee = models.ForeignKey(Attendees, on_delete=models.CASCADE)
    time_in = models.DateTimeField(default= timezone.now)
    
    

    def __str__(self) -> str:
        return f'{self.attendee}'