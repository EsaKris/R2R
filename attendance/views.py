from django.shortcuts import render, redirect
from .models import Attendance, Attendees, CreateAttendance
from .forms import CreateAttendanceForm
from django.contrib import messages

def createAttendance(request):
    if request.user.is_staff:
        attendance = CreateAttendance.objects.all().order_by('-created_date')
        
        if request.method == "POST":
            form = CreateAttendanceForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = CreateAttendanceForm()
        context = {
            'attendance':attendance,
            'form':form,
            }
        return render(request, 'attendance/index.html', context)
    else:
        return redirect('/')
from django.contrib.auth.decorators import login_required
@login_required
def attendanceDetail(request, pk):
    attendance = CreateAttendance.objects.get(pk=pk)
    all = Attendance.objects.filter(attendance=attendance)
    Pastors =[]
    Workers=[]
    Members =[]
    for attendee in all:
        if attendee.attendee.Are_you_a_pastor:
            Pastors.append(attendee)
        elif attendee.attendee.volunteers.Volunteer == True and attendee.attendee.Are_you_a_pastor == False:
            Workers.append(attendee)
        elif attendee.attendee.volunteers.Volunteer == False and attendee.attendee.Are_you_a_pastor == False:
            Members.append(attendee)
    context =  {
             'attendance':attendance,
             'attendance_list': {
                 'all': all,
                 'Pastors':{
                     'all':Pastors,
                     'count':len(Pastors)
                 },
                 'Workers':{
                     'all':Workers,
                     'count':len(Workers)
                 },
                 'Members':{
                     'all':Members,
                     'count':len(Members)
                 }
             }
          }
    return render(request, 'attendance/detail.html', context)

from django.http import JsonResponse

def takeAttendance(request, pk, uid):
    attendance = CreateAttendance.objects.get(pk=pk)
    attendee = Attendees.objects.get(uid=uid)
    attend, created = Attendance.objects.get_or_create(attendance=attendance, attendee=attendee)
    data = {
        'attendee':f'{attend.attendee}',
        'time_in':attend.time_in,
    }
    
    return JsonResponse(data, safe=False, status=200)



from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

def check_male_gender(lists):
    Male =[]
    for person in lists:
        if person.attendee.Gender == "Male":
            Male.append(person)
    return Male

def check_female_gender(lists):
    Female =[]
    for person in lists:
        if person.attendee.Gender == "Female":
            Female.append(person)
    return Female

def add_title( doc, title_text, size=32, bold=True):
    title = doc.add_paragraph()
    title_run = title.add_run(title_text)
    title_run.font.size = Pt(size)
    if bold:
        title_run.bold = True
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return title

def generate_word_doc(request, pk):
    attendance = CreateAttendance.objects.get(pk=pk)
    lists = Attendance.objects.filter(attendance=attendance)
    All= []
    Pastors = []
    Workers  = []
    Members  = []
    for attendee in lists:
        All.append(attendee)
        if attendee.attendee.Are_you_a_pastor:
            Pastors.append(attendee)
        elif attendee.attendee.volunteers.Volunteer == True and attendee.attendee.Are_you_a_pastor == False:
            Workers.append(attendee)
        elif attendee.attendee.volunteers.Volunteer == False and attendee.attendee.Are_you_a_pastor == False:
            Members.append(attendee)
    doc = Document()


    # Add a cover page
    cover_page = doc.sections[0].footer
    cover_page.is_linked_to_previous = False
    cover_page.paragraphs[0].clear()

    title = add_title(doc, f"Again and Afresh Attendance Report \n Gathering of Believers", size=24, bold=True)
    event_name = doc.add_paragraph()
    event_name.add_run(f"Service Title: {attendance.title}").bold = True
    event_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    event_date = doc.add_paragraph()
    event_date.add_run(f"Service Date: {attendance.date.date()}").bold = True
    event_date.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')

    summaryTableHeaderText = doc.add_paragraph()
    summaryTableHeaderText.add_run(f"Summary Table").bold = True
    summaryTable = doc.add_table(rows=5, cols=5)
    summaryTable.style = 'Table Grid'
    for row in summaryTable.rows:
        for cell in row.cells:
            cell.width = Pt(100)
            cell.paragraphs[0].alignment = 1
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        row.cells[0].width = Pt(30)

    summaryTableHeader = summaryTable.rows[0].cells
    summaryTableHeader[0].text = "S/N"
    summaryTableHeader[1].text = "Group"
    summaryTableHeader[2].text = "Male"
    summaryTableHeader[3].text = "Female"
    summaryTableHeader[4].text = "Total"

    summaryTableData = [
        ['1','All', str(len(check_male_gender(All))), str(len(check_female_gender(All))), str(len(All))],
        ['2','Pastor', str(len(check_male_gender(Pastors))), str(len(check_female_gender(Pastors))), str(len(Pastors))],
        ['3','Worker', str(len(check_male_gender(Workers))), str(len(check_female_gender(Workers))), str(len(Workers))],
        ['4','Member', str(len(check_male_gender(Members))), str(len(check_female_gender(Members))), str(len(Members))],
    ]

    for i, row in enumerate(summaryTable.rows[1:], start=1):
        if i - 1 < len(summaryTableData):  # Check if the index is within the range of summaryTableData
            for j, cell in enumerate(row.cells):
                if j < len(summaryTableData[i-1]):  # Check if the index is within the range of summaryTableData[i-1]
                    cell.text = summaryTableData[i-1][j]

    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    ds = len(Pastors) + 2

    add_title(doc, f"Pastors List", size=18, bold=True)
    PastorsTable = doc.add_table(rows=ds, cols=5)
    PastorsTable.style = 'Table Grid'

    for row in PastorsTable.rows:
        for cell in row.cells:
            cell.width = Pt(100)
            cell.paragraphs[0].alignment = 1
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        row.cells[0].width = Pt(30)

    PastorsTableHeader = PastorsTable.rows[0].cells
    PastorsTableHeader[0].text = "S/N"
    PastorsTableHeader[1].text = "Name"
    PastorsTableHeader[2].text = "Phone"
    PastorsTableHeader[3].text = "Gender"
    PastorsTableHeader[4].text = "Time"

    PastorsTableData =[]
    for index, member in enumerate(Pastors):
        sn = index +1
        PastorsTableData.append(
            [str(sn), f'{member.attendee.Full_Name.title()}', str(member.attendee.Phone), str(member.attendee.Gender), str(member.time_in.time())]
        )
       
    for i, row in enumerate(PastorsTable.rows[1:], start=1):
        if i - 1 < len(PastorsTableData):  # Check if the index is within the range of PastorsTableData
            for j, cell in enumerate(row.cells):
                if j < len(PastorsTableData[i-1]):  # Check if the index is within the range of PastorsTableData[i-1]
                    cell.text = PastorsTableData[i-1][j]


    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    ds = len(Workers) + 2

    add_title(doc, f"Workers List", size=18, bold=True)
    WorkersTable = doc.add_table(rows=ds, cols=5)
    WorkersTable.style = 'Table Grid'

    for row in WorkersTable.rows:
        for cell in row.cells:
            cell.width = Pt(100)
            cell.paragraphs[0].alignment = 1
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        row.cells[0].width = Pt(30)

    WorkersTableHeader = WorkersTable.rows[0].cells
    WorkersTableHeader[0].text = "S/N"
    WorkersTableHeader[1].text = "Name"
    WorkersTableHeader[2].text = "Phone"
    WorkersTableHeader[3].text = "Gender"
    WorkersTableHeader[4].text = "Time"

    WorkersTableData =[]
    for index, member in enumerate(Workers):
        sn = index +1
        WorkersTableData.append(
            [str(sn), f'{member.attendee.Full_Name.title()}', str(member.attendee.Phone), str(member.attendee.Gender), str(member.time_in.time())]
        )
       
    for i, row in enumerate(WorkersTable.rows[1:], start=1):
        if i - 1 < len(WorkersTableData):  # Check if the index is within the range of WorkersTableData
            for j, cell in enumerate(row.cells):
                if j < len(WorkersTableData[i-1]):  # Check if the index is within the range of WorkersTableData[i-1]
                    cell.text = WorkersTableData[i-1][j]
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    ds = len(Members) + 2

    add_title(doc, f"Non-workers/Members", size=18, bold=True)
    MembersTable = doc.add_table(rows=ds, cols=4)
    MembersTable.style = 'Table Grid'

    for row in MembersTable.rows:
        for cell in row.cells:
            cell.width = Pt(100)
            cell.paragraphs[0].alignment = 1
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        row.cells[0].width = Pt(30)

    MembersTableHeader = MembersTable.rows[0].cells
    MembersTableHeader[0].text = "S/N"
    MembersTableHeader[1].text = "Name"
    MembersTableHeader[2].text = "Phone Number"
    MembersTableHeader[3].text = "Time"

    MembersTableData =[]
    for index, member in enumerate(Members):
        MembersTableData.append(
            [str(index + 1), f'{member.attendee.last_name.title()} {member.attendee.first_name.title()}', str(member.attendee.phone), str(member.time_in.time())]
        )
    for i, row in enumerate(MembersTable.rows[1:], start=1):
        if i - 1 < len(MembersTableData):  # Check if the index is within the range of MembersTableData
            for j, cell in enumerate(row.cells):
                if j < len(MembersTableData[i-1]):  # Check if the index is within the range of MembersTableData[i-1]
                    cell.text = MembersTableData[i-1][j]
    doc.save(f"Attendance_list/Attendance {attendance.id} for {attendance.title} {attendance.date.date()}.docx")
    print("save")
    messages.success(request, f"You have successfull generated Attendance {attendance.id} for {attendance.title} {attendance.date.date()}.docx")
    return redirect("attendance-list")