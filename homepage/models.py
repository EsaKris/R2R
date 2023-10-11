from django.db import models
from django.utils import timezone

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Attendees(models.Model):
    Full_Name = models.CharField(max_length=250)
    Email = models.EmailField()
    Phone = models.CharField(max_length=20)
    Gender = models.CharField(max_length = 150, choices=GENDER)
    Local_Assembly = models.CharField(max_length=250)
    
    Nationality = models.CharField(max_length=100)
    State_of_Origin = models.CharField(max_length=100)
    Local_Government_Area = models.CharField(max_length=200)

    Are_you_a_pastor = models.BooleanField(default=False)
    will_you_be_camping = models.BooleanField(default=False)

    created = models.DateTimeField(default = timezone.now())    

    def __str__(self):
        return f'{self.Full_Name}'
    

class Volunteers(models.Model):
    Attendee = models.ForeignKey(Attendees, on_delete=models.CASCADE)
    created = models.DateTimeField(default = timezone.now())    
    
    def __str__(self):
        return f'{self.Attendee}'