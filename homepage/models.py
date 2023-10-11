from django.db import models

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
    
    

    