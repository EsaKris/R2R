from django import forms
from .models import Attendees, Volunteers, prayerRequest, Specialcard, InHouse

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendees
        fields = ('Full_Name','Email', 'Phone', 'Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')

class VolunteersForm(forms.ModelForm):
    class Meta:
        model = Volunteers
        fields =  ('Volunteer',)


class RequestsForm(forms.ModelForm):
    class Meta:
        model = prayerRequest
        fields =  ('Full_Name','Request')

class SpecialCardForm(forms.ModelForm):
    class Meta:
        model = Specialcard
        fields = ('name','level','title','church')

class InhouseForm(forms.ModelForm):
    class Meta:
        model = InHouse
        fields = ('person','department','brethren',)