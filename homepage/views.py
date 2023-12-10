from django.shortcuts import render, redirect
from .forms import AttendeeForm, VolunteersForm, RequestsForm, SpecialCardForm, InhouseForm
from .models import Attendees, Specialcard
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

def donate(request):
    return render(request, "home/donate.html")

def AttendeeListView(request):
    if request.user.is_staff:
        specialcard = Specialcard.objects.all().order_by('-created')
        Attendee = Attendees.objects.all().order_by('-created')
        for attendee in Attendee:
            if len(str(attendee.id)) == 4:
                attendee.id
            elif len(str(attendee.id)) == 3:
                attendee.id = f"0{attendee.id}"
            elif len(str(attendee.id)) == 2:
                attendee.id = f"00{attendee.id}"
            elif len(str(attendee.id)) == 1:
                attendee.id = f"000{attendee.id}"
        for attendee in specialcard:
            if len(str(attendee.id)) == 4:
                attendee.id
            elif len(str(attendee.id)) == 3:
                attendee.id = f"0{attendee.id}"
            elif len(str(attendee.id)) == 2:
                attendee.id = f"00{attendee.id}"
            elif len(str(attendee.id)) == 1:
                attendee.id = f"000{attendee.id}"
        if request.method == "POST":
            form = SpecialCardForm(request.POST)
            if form.is_valid():
                data = form.save()
                messages.success(request, f'You have successfully created a specialcard with and id of: {data.id}')
                return redirect('AttendeeListView')
        else:
            form = SpecialCardForm()
    else:
        return redirect('/')
    return render(request, "home/attendee_list.html", {'Attendee':Attendee, 'form':form, 'specialcard':specialcard})    

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

def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})

def inhouse(request):
    if request.method == "POST":
        form = InhouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = InhouseForm()
    return render(request, "home/inhouseform.html", {'form':form})
