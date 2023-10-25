from django.shortcuts import render, redirect
from .forms import AttendeeForm, VolunteersForm, RequestsForm
from .models import Attendees
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form =AttendeeForm(request.POST)
        if form.is_valid():
            data = form.save()
            return redirect('volunteer', pk = data.id)
    else:
        form =AttendeeForm()
    return render(request, 'home/register.html', {'form':form})

def volunteer(request, pk):
    
    Attendee = Attendees.objects.filter(pk=pk)
    if Attendee:
        Attendee = Attendees.objects.get(pk=pk)
        if request.method == "POST":
            form = VolunteersForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                f.Attendee = Attendee
                data = form.save()
                messages.success(request, f"Hello {data.Attendee.Full_Name}, Congratulation You have successfully registered for R2R 2023 Your ID is {data.Attendee.id}")
            return redirect('/')
        else:
            form = VolunteersForm(request.POST)
    else:
        return redirect('/')
    return render(request, "home/volunteer.html", {'form':form})


def prayerRequest(request):
    if request.method == "POST":
        form = RequestsForm(request.POST)
        if form.is_valid():
            data = form.save()
            messages.success(request, f'Hello {data.Full_Name}, your prayer request has been sent.')
    return redirect('/')        

def homepage(request):
    return render(request, "home/index.html")

def AttendeeListView(request):
    if request.user.is_staff:
        Attendee = Attendees.objects.all().order_by('-created')
    else:
        return redirect('/')
    return render(request, "home/attendee_list.html", {'Attendee':Attendee, 'form':AttendeeForm()})    

from django.db.models import Q
from django.http import JsonResponse
def search_fields(request):
    query = request.POST.get('search')
    if query == None:
        return redirect('AttendeeListView/')
    print(query)
    Attendee = Attendees.objects.filter(Q(Full_Name__icontains = query))
    data = []
    for attendee in Attendee:
        date = f'{attendee.created.day}/{attendee.created.month}/{attendee.created.year}'
        data.append({
            'Full_Name' : attendee.Full_Name,
            'Email' : attendee.Email,
            'Phone' : attendee.Phone,
            'Gender' : attendee.Gender,
            'Local_Assembly' : attendee.Local_Assembly,
            'Nationality' : attendee.Nationality,
            'State_of_Residence' : attendee.State_of_Residence,
            'Local_Government_Area' : attendee.Local_Government_Area,
            'Are_you_a_pastor' : attendee.Are_you_a_pastor,
            'will_you_be_camping' : attendee.will_you_be_camping,
            'created' : date
        })
    return render(request, "home/attendee_list.html", {'Attendee':Attendee, 'form':AttendeeForm()})    
