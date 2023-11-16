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
    
    for attendee in all:
        try:
            if attendee.attendee.isPastor:
                Pastors.append(attendee)
        except:
            if attendee.attendee.role == "WORKER" or attendee.attendee.role == "HOU" or attendee.attendee.role == "HOD":
                Workers.append(attendee)
            else:
                Members.append(attendee)
    context =  {
             'attendance':attendance,
             'attendance_list': {
                 'all': all,
             }
          }
    return render(request, 'attendance/detail.html', context)



from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


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
        try:
            if attendee.attendee.Are_you_a_pastor:
                Pastors.append(attendee)
        except:
            if attendee.attendee.volunteers.Volunteer == True and attendee.attendee.Are_you_a_pastor == False:
                Workers.append(attendee)
            elif attendee.attendee.volunteers.Volunteer == False and attendee.attendee.Are_you_a_pastor == False:
                Members.append(attendee)
    doc = Document()


    # Add a cover page
    cover_page = doc.sections[0].footer
    cover_page.is_linked_to_previous = False
    cover_page.paragraphs[0].clear()

    title = add_title(doc, f"Layers of Truth Attendance Report \n {attendance.title}", size=24, bold=True)
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

    data = [
        ['1','All', str(len(check_male_gender(All))), str(len(check_female_gender(All))), str(len(All))],
        ['2','Pastor', str(len(check_male_gender(Pastors))), str(len(check_female_gender(Pastors))), str(len(Pastors))],
        ['3','Worker', str(len(check_male_gender(Workers))), str(len(check_female_gender(Workers))), str(len(Workers))],
        ['4','Member', str(len(check_male_gender(Members))), str(len(check_female_gender(Members))), str(len(Members))],
    ]

    
    doc.add_paragraph('')
    doc.add_paragraph('')
    doc.add_paragraph('')
    depttitle = doc.add_paragraph()
    depttitle.add_run(f"Department Summary Table").bold = True
    ds = department.count() + 2

    summarydepartmentTable = doc.add_table(rows=ds, cols=5)
    summarydepartmentTable.style = 'Table Grid'

    for row in summarydepartmentTable.rows:
        for cell in row.cells:
            cell.width = Pt(100)
            cell.paragraphs[0].alignment = 1
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        row.cells[0].width = Pt(30)

    summarydepartmentTableHeader = summarydepartmentTable.rows[0].cells
    summarydepartmentTableHeader[0].text = "S/N"
    summarydepartmentTableHeader[1].text = "Department"
    summarydepartmentTableHeader[2].text = "Male"
    summarydepartmentTableHeader[3].text = "Famale"
    summarydepartmentTableHeader[4].text = "Total"

    summarydepartmentTableData =[]
    
    doc.add_page_break()
    add_title(doc, f"Department List", size=18, bold=True)
    for index, dept in enumerate(department):
        
        depttitle = doc.add_paragraph()
        depttitle.add_run(f"{dept.name.title()}").bold = True

        departmentLists = []
        primarywork = primaryWork.objects.filter(worker__department = dept)
        for item in lists:
            for work in primarywork:
                if item.attendee.username == work.user.username:    
                    departmentLists.append(item)
        row = len(departmentLists) + 2
        departmentTable = doc.add_table(rows=row, cols=5)
        departmentTable.style = 'Table Grid'
        
        for row in departmentTable.rows:
            for cell in row.cells:
                cell.width = Pt(100)
                cell.paragraphs[0].alignment = 1
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            row.cells[0].width = Pt(30)

        departmentTableHeader = departmentTable.rows[0].cells
        departmentTableHeader[0].text = "S/N"
        departmentTableHeader[1].text = "Name"
        departmentTableHeader[2].text = "Department"
        departmentTableHeader[3].text = "Unit"
        departmentTableHeader[4].text = "Time"

        deptpeople = []
        deptdata = []
        
        for i, attendee in enumerate(departmentLists):
            sn = i+1
            if attendee.attendee.primarywork.worker.department.id == dept.id:
                for item in lists:
                    if item.attendee == attendee.attendee:
                        deptpeople.append(attendee)
                deptdata.append(
                    [str(sn), f'{attendee.attendee.last_name.title()} {attendee.attendee.first_name.title()}', str(attendee.attendee.primarywork.worker.department), str(attendee.attendee.primarywork.worker.unit), str(attendee.time_in.time())]
                )
            else:
                Members.append(attendee)
        for i, row in enumerate(departmentTable.rows[1:], start=1):
            if i - 1 < len(deptdata):  # Check if the index is within the range of deptdata
                for j, cell in enumerate(row.cells):
                    if j < len(deptdata[i-1]):  # Check if the index is within the range of deptdata[i-1]
                        cell.text = deptdata[i-1][j]
        dept_id  = index +1
        
        summarydepartmentTableData.append(
            [f'{dept_id}', f'{dept.name.title()}', str(len(check_male_gender(deptpeople))), str(len(check_female_gender(deptpeople))), str(len(deptpeople)) ]
        )
        
        
        for i, row in enumerate(summaryTable.rows[1:], start=1):
            for j, cell in enumerate(row.cells):
                cell.text = data[i-1][j]

        doc.add_paragraph('')
        doc.add_paragraph('')

   
    for i, row in enumerate(summarydepartmentTable.rows[1:], start=1):
            if i - 1 < len(summarydepartmentTableData):  # Check if the index is within the range of summarydepartmentTableData
                for j, cell in enumerate(row.cells):
                    if j < len(summarydepartmentTableData[i-1]):  # Check if the index is within the range of summarydepartmentTableData[i-1]
                        cell.text = summarydepartmentTableData[i-1][j]


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
    PastorsTableHeader[2].text = "Department"
    PastorsTableHeader[3].text = "Unit"
    PastorsTableHeader[4].text = "Time"

    PastorsTableData =[]
    for index, member in enumerate(Pastors):
        sn = index +1
        try:
            PastorsTableData.append(
                [str(sn), f'{member.attendee.last_name.title()} {member.attendee.first_name.title()}', str(member.attendee.primarywork.worker.department), str(member.attendee.primarywork.worker.unit), str(member.time_in.time())]
            )
        except:
            PastorsTableData.append(
                [str(sn), f'{member.attendee.last_name.title()} {member.attendee.first_name.title()}', "None", "None", str(member.time_in.time())]
            )
    for i, row in enumerate(PastorsTable.rows[1:], start=1):
        if i - 1 < len(PastorsTableData):  # Check if the index is within the range of PastorsTableData
            for j, cell in enumerate(row.cells):
                if j < len(PastorsTableData[i-1]):  # Check if the index is within the range of PastorsTableData[i-1]
                    cell.text = PastorsTableData[i-1][j]


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
    doc.save(f"Attendance_list/Attendance {attendance.id} for {attendance.name} {attendance.date.date()}.docx")
    print("save")
    messages.success(request, f"You have successfull generated Attendance {attendance.id} for {attendance.name} {attendance.date.date()}.docx")
    return redirect("attendance-list")