from django.db import models
from django.utils import timezone
import uuid
from qrcode import *
from .countries import countryListAlpha3

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class Attendees(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    Full_Name = models.CharField(max_length=250, null=True, blank=True)
    Email = models.EmailField(unique=True, null=True, blank=True)
    Phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    Gender = models.CharField(max_length = 150, choices=GENDER, null=True, blank=True)
    Local_Assembly = models.CharField(max_length=250, null=True, blank=True)
    
    Nationality = models.CharField(max_length=100, choices=countryListAlpha3, null=True, blank=True)
    State_of_Residence = models.CharField(max_length=100, null=True, blank=True)
    Local_Government_Area = models.CharField(max_length=200, null=True, blank=True)

    Are_you_a_pastor = models.BooleanField(default=False, verbose_name="Are you a pastor?")
    will_you_be_camping = models.BooleanField(default=False, verbose_name="will you be camping with us?")

    created = models.DateTimeField(auto_now_add=True)    

    def qr_code(self):
        qr_code = make(self.uid)

        basename = str(self.Full_Name.replace(" ", "_")) + '_QR_CODE.png'
        qr_code.save('media/QR_CODE/{}'.format(basename))
        return '/media/QR_CODE/{}'.format(basename)

    def __str__(self):
        return f'{self.Full_Name} -> ID:{self.id}'
    
    def save(self,force_insert=True,using='dataset'):
        super().save(force_insert)

    def save(self, *args, **kwargs):
        self.qr_code()
        return super().save(*args, **kwargs)

class Volunteers(models.Model):
    Attendee = models.OneToOneField(Attendees, on_delete=models.CASCADE, related_name='volunteers',null=True,blank=True)
    Volunteer = models.BooleanField(default=False)
    created = models.DateTimeField(default = timezone.now())    
    
    def __str__(self):
        return f'{self.Attendee}'


class prayerRequest(models.Model):
    Full_Name = models.CharField(max_length=250)
    Request = models.TextField()
    created = models.DateTimeField(default = timezone.now())    
    
    def __str__(self):
        return f'{self.Full_Name}'
    
levels = (
    ('1','Level 1'),
    ('2','Level 2'),
    ('3','Level 3'),
)
class Specialcard(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    level = models.CharField(max_length=8, choices=levels)
    title = models.CharField(max_length=255)
    church = models.CharField(max_length=255)
    created = models.DateTimeField(default = timezone.now())
    
    def qr_code(self):
        qr_code = make(self.uid)
        basename = str(self.name.replace(" ", "_")) + '_QR_CODE.png'
        qr_code.save('media/QR_CODE/{}'.format(basename))
        return '/media/QR_CODE/{}'.format(basename)

    def __str__(self):
        return f'{self.name} -> ID:{self.id}'
    
    def save(self,force_insert=True,using='dataset'):
        super().save(force_insert)

    def save(self, *args, **kwargs):
        self.qr_code()
        return super().save(*args, **kwargs)
    
class InHouse(models.Model):
    person = models.OneToOneField(Attendees, on_delete=models.CASCADE, related_name="inhouse")
    department = models.CharField(max_length=255, verbose_name="Enter your department name")
    brethren = models.BooleanField(default=False, verbose_name="Are you an inhouse brethen?")

    def __str__(self):
        return f'{self.person}'
    