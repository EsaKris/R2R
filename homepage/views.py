from django.shortcuts import render
from .forms import AttendeeForm

def register(request):
    if request.method == "POST":
        form =AttendeeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form =AttendeeForm()
    return render(request, 'home/register.html', {'form':form})