from django import forms
from .models import Attendees

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendees
        fields = ('Full_Name','Email', 'Phone', 'Gender','Local_Assembly', 'Nationality', 'State_of_Residence', 'Local_Government_Area', 'Are_you_a_pastor', 'will_you_be_camping')