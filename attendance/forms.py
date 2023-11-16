from django import forms
from .models import CreateAttendance

class CreateAttendanceForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = CreateAttendance
        fields = ('title','date',)