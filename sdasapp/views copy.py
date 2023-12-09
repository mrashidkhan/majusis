from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .models import Student
from sdasapp import *
from django.contrib.auth.models import User
from django.views.generic import View

# from .forms import DepartmentForm, FacultyForm
from .forms import *

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# def validate_code_length(value):
#     if len(value) < 4:
#         raise ValidationError(
#             _('%(value)s is less than 4'),
#             params={'value': value},
#         )

def index(request):
    return render(request, 'index.html')

def dual_listbox(request):
    return render(request, 'dual_listbox.html')

def user_signin(request):
    error = ""
    d = {}
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['password']
        user = authenticate(username=u, password=p)

        if user:
            try:
                login(request, user)
                error = "no"
                response = redirect('/index/')
                return response
            except:
                error = "yes"
        else:
            error = "yes"
        d = {'error': error}
    return render(request, 'user_signin.html', d)

def register_complain(request):
    return render(request, 'register_complain.html')


def change_password(request):
    error = ""
    d = {}
    if request.method == 'POST':
        # {{user.first_name}} {{user.last_name}}
        # u = request.POST['uname']
        p = request.POST['cpwd']
        np = request.POST['npwd']

        user = authenticate(username={request.user.username}, password=p)

        try:
            if user:
                appuser = AppUser.objects.get(user=user)
                error = "no"
                # user.set_password({np})
                appuser.password = np
                messages.info(request, "You have successfully changed the password.")
                appuser.save()
            else:
                error = "yes"
        except:
            error = "no"

    d = {'error': error}
    return render(request, 'change_password.html', d)
    return render(request, 'change_password.html')

def user_signout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return render(request, 'user_signin.html')


def user_signup(request):
    error = "no"
    d = {}
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact_no']
        dept = request.POST['dept']
        gen = request.POST['genderRadios']
        desig = request.POST['desig']
                
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            AppUser.objects.create(user_id=user.id, contact_no=con, gender=gen, dept_id=dept,desig=desig)
            error="no"
        except:
            error="yes"

        d = {'error': error}
    return render(request, 'user_signup.html', d)
   
def faculty_read(request):
    context = {'faculty_data':Faculty.objects.all()}
    return render(request, "faculty_read.html",context)

def add_faculty(request):
    if request.method == "POST":
        try:
            faculty_name = request.POST['faculty_name']
            Faculty.objects.create(
            faculty_name=faculty_name
            )
            messages.warning(request, 'Faculty record has been added.')
            return render(request, "add_faculty.html")
        # , {'msg':'Faculty has been added'}
        except: 
            messages.warning(request, 'There is a problem with entered Faculty record information.')
            return render(request, "add_faculty.html", {'msg':'Error: Provide all information to create Faculty record'})
    else:
        return render(request, "add_faculty.html")

def designation_read(request):
    context = {'designation_data':Designation.objects.all()}
    return render(request, "designation_read.html",context)

def designation_delete(request, id):
        if request.method == 'POST':
            designation = Designation.objects.get(pk=id)
            designation.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Designation record has been deleted.')
        response = redirect('/designation_read/')
        return response

def add_designation(request):
    if request.method == "POST":
        try:
            designation_name = request.POST['designation_name']
            comments = request.POST['comments']
            Designation.objects.create(
            designation_name = designation_name,
            comments = comments
            )
            messages.warning(request, 'designation record has been added.')
            return render(request, "add_designation.html")
        
        except: 
            messages.warning(request, 'There is a problem with entered designation record information.')
            return render(request, "add_designation.html", {'msg':'Error: Provide all information to create designation record'})
    else:
        return render(request, "add_designation.html")
 
def dept_read(request):
    context = {'dept_read':Dept.objects.all()}
    return render(request, "dept_read.html",context)

def add_dept(request):
    if request.method == "POST":
            form = DeptForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Department record has been submitted Successfully ")
            else:
                messages.success(request, "There was an error in your form! Please try again...")
            return redirect('add_dept')
            
            messages.success(request, "Department record has been submitted Successfully ")
            return redirect(request, 'dept_read')
    else:
        form = DeptForm()
        return render(request, "add_dept.html", {'form':form})
    
def term_read(request):
    context = {'term_read':Term.objects.all()}
    return render(request, "term_read.html",context)

def add_term(request):
    if request.method == "POST":
            form = TermForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Term record has been submitted Successfully ")
            else:
                messages.success(request, "There was an error in your form! Please try again...")
            return redirect('add_term')
            
            messages.success(request, "Term record has been submitted Successfully ")
            return redirect(request, 'term_read')
    else:
        form = TermForm()
        return render(request, "add_term.html", {'form':form})
    
def offence_read(request):
    context = {'offence_data':Offence.objects.all()}
    return render(request, "offence_read.html",context)

def add_offence(request):
    if request.method == "POST":
        form = OffenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Offence record has been submitted Successfully!'))
            return redirect('offence_read')
        else:
            messages.success(request, ('There was an error in your form! Please try again...'))
            return redirect('add_offence')
    else:
        form = OffenceForm()
        return render(request, "add_offence.html", {'form':form})


# def add_program_type(request):
#     return render(request, 'add_program_type.html')

# def add_program(request):
#     return render(request, 'add_program.html')

# def add_program_type(request):
#     if request.method == "POST":
#         try:
#             form = Program_typeForm(request.POST)
#             if form.is_valid():
#                 form.save()
#             return redirect('program_type_read')
#         except:
            
#     else:
#         form = Program_typeForm()
#         return render(request, "add_program_type.html", {'form':form})

# def program_type_read(request):
#     context = {'program_read':Program.objects.all()}
#     return render(request, "program_read.html",context)
    
# def add_program(request):
#     if request.method == "POST":
#         form = Program_Form(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('program_type_read')
#     else:
#         form = ProgramForm()
#         return render(request, "add_program_type.html", {'form':form})
    
def add_program(request):
    if request.method == "POST":
        # try:
            
            form = ProgramForm(request.POST)
            if form.is_valid():
                error = {'msg':'Data has problem, try again'}
                form.save()
                messages.success(request, "Program record has been added Successfully.")
                # form = ProgramForm()
            return render(request, "add_program.html", {'form':form})
        # ,'msg':'Program has been added'
        # except: 
            messages.success(request, "Entered record information has problem")
            return render(request, "add_program.html", {'form':form})
    else:
        form = ProgramForm()
        return render(request, "add_program.html", {'form':form,'msg':''})
        
def program_read(request):
    context = {'program_read':Program.objects.all()}
    return render(request, "program_read.html",context)
    

    
# def add_program(request):
#     if request.method == "POST":
#         return render(request, "add_program.html", {'programs':Program.objects.all() })
#     else:
#         return render(request, "add_program.html", {'programs':Program.objects.all() })

# def program_read(request):
#     context = {'program_read':Program.objects.all()}
#     return render(request, "program_read.html",context)
    
# def add_program(request):
#     if request.method == "POST":
#         try:
#             program_name = request.POST['program_name']
#             dept = Program.objects.get(dept=dept)
#             Program.objects.create(
#                 program_name=program_name,
#                 program_type=program_type,
#                 dept = dept,
#             )
#             return render(request, "add_program.html", {'msg':'Program has been added','depts':Department.objects.all()})
#         except: 
#             return render(request, "add_program.html", {'msg':'Error: Provide all information to create Program record','depts':Department.objects.all()})
#     else:
#         return render(request, "add_program.html", {'depts':Department.objects.all()})
        
    
# def program_read(request):
#     context = {'program_read':Program.objects.all()}
#     return render(request, "program_read.html",context)
    

# def add_student(request):
#     return render(request, 'add_student.html')

# def add_student(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('student_read')
#     else:
#         form = StudentForm()
#         return render(request, "add_student.html", {'form':form})

def add_student(request):
    context = {}
    if request.method == "POST":
        # try:
            term_id = request.POST.get("term")
            term = Term.objects.get(id=term_id)
            program_id = request.POST.get("program")
            program = Program.objects.get(id=program_id)
            rollnumber = request.POST['rollnumber']
            
            temp = str(term) + '-' + str(program) + '-' + str(rollnumber)  
            student_id = str(temp)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_type = 'Student'
            email_id = request.POST['email_id']
            contact_no = request.POST['contact_no']
            gender = request.POST['gender']
            
                    
            student_user = Student(
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                user_type=user_type,
                contact_no=contact_no,
                gender=gender,
                student_id=student_id,
                program=program,
                term=term)
            
            student_user.save()
            
            messages.success(request, "Student record has been added Successfully.")
            context = {'programs':Program.objects.all(), 'terms':Term.objects.all() }
            return render(request, "add_student.html", context)
        
        # except: 
            messages.success(request, "Entered record information has problem")
            return render(request, "add_student.html", context)
    else:
        context = {'programs':Program.objects.all(), 'terms':Term.objects.all() }
        return render(request, "add_student.html", context)
        
    
def student_read(request):
    context = {'student_read':Student.objects.all()}
    return render(request, "student_read.html",context)

# def add_staff(request):
#     if request.method == "POST":
#         try:
#             first_name = request.POST['first_name']
#             last_name = request.POST['last_name']
#             email_id = request.POST['email_id']
#             staff_id = request.POST['staff_id']
#             user_type = 'Staff'
            
#             contact_no = request.POST['contact_no']
#             gender = request.POST['gender']
#             designation = request.POST['designation']
#             designationobj = Designation.objects.get(id=designation)
#             deptid = request.POST['dept']
#             deptobj = Dept.objects.get(id=deptid)
#             staff_user = Staff(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email_id=email_id,
#                 staff_id=staff_id,
#                 user_type=user_type,
#                 contact_no=contact_no,
#                 gender=gender,
#                 designation=designationobj,
#                 )
            
#             staff_user.save()
#             staff_user.depts.add(deptobj)
            
#             messages.success(request, "Staff record has been added Successfully.")
#             context = {'depts':Dept.objects.all(),'designations':Designation.objects.all()}
#             return render(request, "add_staff.html", context)
#         except:
#             messages.success(request, "Entered record information has problem")
#             context = {'depts':Dept.objects.all(),'designations':Designation.objects.all()}
#             return render(request, "add_staff.html", context)
        
#     else:
#         context = {'depts':Dept.objects.all(),'designations':Designation.objects.all()}
#         return render(request, "add_staff.html", context)

def add_staff(request):
    if request.method == "POST":
            form = StaffForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Staff record has been submitted Successfully ")
            else:
                messages.success(request, "There was an error in your form! Please try again...")
            return redirect('add_staff')
            
            messages.success(request, "Staff record has been submitted Successfully ")
            return redirect(request, 'staff_read')
    else:
        form = StaffForm()
        return render(request, "add_staff.html", {'form':form})        
    
def staff_read(request):
    context = {'staff_read':Staff.objects.all()}
    return render(request, "staff_read.html",context)

def add_facultymember(request):
    if request.method == "POST":
            form = FacultyMemberForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Faculty member record has been submitted Successfully ")
                return redirect('add_facultymember')
            else:
                messages.success(request, "There was an error in your form! Please try again...")
                return redirect('facultymember_read')
            
            # messages.success(request, "Faculty Member record has been submitted Successfully ")
            
    else:
        form = FacultyMemberForm()
        return render(request, "add_facultymember.html", {'form':form})        
    
def facultymember_read(request):
    context = {'facultymember_read':FacultyMember.objects.all()}
    return render(request, "facultymember_read.html",context)

def multi_select(request):
    return render(request, "multi_select.html")

# complain_id = models.AutoField(primary_key=True)
# complain_detail = models.CharField(max_length=255)
# complalin_date = models.DateTimeField()
# complainant = models.ForeignKey(AppUser, on_delete=models.CASCADE)
# register_by = models.ForeignKey(User, on_delete=models.CASCADE ) 

def add_complain(request):
    offenders = Student.objects.all()
    complainant = Student.objects.all()
    offences = Offence.objects.all()
    # if 'q' in request.GET:
    #     q = request.GET['q']
         
    # else: 
    #     context = {}      
    #     offenders = Student.objects.all()
    #     complainant = Student.objects.all()  
    #     offences = Offence.objects.all()  
            
        # if request.method == "GET":
            
        #     complainant = Student.objects.all()  
        #     offences = Offence.objects.all() 
        #     q = request.GET.get('q')
        #     if q != None:
            
        #        offenders = Student.objects.filter(student_id__icontains=q)
        # context = {'complainant':complainant,'offenders':offenders,'offences':offences}
        # return render(request, "add_complain.html", context)
                                          
    if request.method == "POST":
        # term_id = request.POST.get("term")
        # term = Term.objects.get(id=term_id)
        # try:
            complain_date  = request.POST.get("complain_date") 
            complain_detail  = request.POST.get("complain_detail")                           
            complainant_id  = request.POST.get("complainant")
            complainant = Student.objects.get(id=complainant_id)
            # offenders_id = request.POST.get('offenders')
            # offenders = Student.objects.get(id=offenders_id)
            
            complain_detail = request.POST['complain_detail']
            complain_date = request.POST['complain_date']
            # offences = request.POST.get('offences')
            complain_registered = Complain.objects.create(
            complain_detail=complain_detail,
            complain_date=complain_date,
            complainant = complainant, 
            
            )
            offenders_list = request.POST.get('offenders')
            offences_list = request.POST.get('offences')
            
            # offender_list = []
            # for y in 
            for x in offenders_list:
	            complain_registered.offenders.add(Student.objects.get(id=x))
                # print(complain_registered.offenders.all())
                
            for x in offences_list:
	            complain_registered.offences.add(Offence.objects.get(id=x))
                # print(complain_registered.offences.all())
        
            offenders = Student.objects.all()
            complainant = Student.objects.all()
            offences = Offence.objects.all()
    
            context = {'msg':'Complain has been added','complainant':complainant,'offenders':offenders,'offences':offences}
            return render(request, "add_complain.html", context)
        # except: 
            offenders = Student.objects.all()
            complainant = Student.objects.all()
            offences = Offence.objects.all()
            context = {'msg':'Error: Provide all information to create Complain','complainant':complainant,'offenders':offenders,'offences':offences}
            return render(request, "add_complain.html", context)

    context = {'complainant':complainant,'offenders':offenders,'offences':offences}
    return render(request, "add_complain.html", context)
        

def search_student(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Student.objects.filter(student_id__icontains=q)  
    else:
        data= Data.objects.all()
    context = {'data':data}
    return render(request, "add_complain.html", context ) 
        


# def add_complain(request):
    
#     # if request.method == "GET":
#     #     searching = request.GET.get('searching')
#     #     offenders = Student.objects.filter(student_id=searching)
    
#     if 'q' in request.GET:
#         q = request.GET['q']
#         offenders = Student.objects.filter(student_id__icontains=q)                         
    
#     if request.method == "POST":
       
#         form = ComplainForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Complain record has been added Successfully.")
#         return redirect('add_complain')
#     else:
#         form = ComplainForm()
#         return render(request, "add_complain.html", {'form':form,'msg':''})
        
def complain_read(request):
    context = {'complain_read':Complain.objects.all()}
    return render(request, "complain_read.html",context)

# def add_meeting(request):
#     return render(request, 'add_meeting.html')

# def add_meeting(request):
#     if request.method == "POST":
#         try:
#             meeting_date = request.POST['meeting_date']
#             meeting_location = request.POST['meeting_location']
#             chair_by = Staff.objects.get(chair_by=chair_by)
#             comments = request.POST['comments']
            
#             meeting_new = Meeting.objects.create(
#             meeting_date=meeting_date,
#             meeting_location=meeting_location,
#             chair_by=chair_by,
#             comments=comments,
#             )
#             return render(request, "add_meeting.html", {'msg':'Meeting has been added','chair_by':Staff.objects.all()})
#         except: 
#             return render(request, "add_meeting.html", {'msg':'Error: Provide all information to create Meeting Record','chair_by':Staff.objects.all()})
#     return render(request, "add_meeting.html", {'chair_by':Staff.objects.all() })
       
def add_meeting(request):
    if request.method == "POST":
       
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Meeting record has been added Successfully.")
        return render(request, "add_meeting.html",{'form':form,'chair_by':Staff.objects.all()})
    # ,'msg':'Meeting has been added'
    else:
        form = MeetingForm()
        return render(request, "add_meeting.html", {'form':form,'chair_by':Staff.objects.all(),'msg':''})
        
def meeting_read(request):
    context = {'meeting_read':Meeting.objects.all()}
    return render(request, "meeting_read.html",context)

    
# def meeting_read(request):
#     context = {'meeting_read':Meeting.objects.all()}
#     return render(request, "meeting_read.html",context)

# def add_meeting(request):
#     if request.method == "POST":
       
#         form = MeetingForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('/meeting_read')
#     else:
#         form = MeetingForm()
#         return render(request, "add_meeting.html", {'form':form})

# def meeting_read(request):
#     context = {'meeting_read':Meeting.objects.all()}
#     return render(request, "meeting_read.html",context)


# def add_attendance(request):
#     return render(request, 'add_attendance.html')
# def attendance_read(request):
#     return render(request, 'attendance_read.html')


# custom_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
#     ATTENDANCE_CHOICES = (
#         ('A', 'Absent'),
#         ('P', 'Present'),
#     )
#     attendance_status = models.CharField(max_length=200, choices=ATTENDANCE_CHOICES)
#     Attendance_comments = models.CharField(max_length=255)


# def add_attendance(request):
#     if request.method == "POST":
#         try:
                       
#             attendance_id = request.POST['attendance_id'] 
            
#             attendee = request.POST['attendee'] 
            
#             meeting = request.POST['meeting']
            
#             attendance_status = request.POST['attendance_status']
                        
#             attendance_comments = request.POST['attendance_comments']
           
            
#             att_record = Attendance.objects.create(
#             attendance_id,
#             meetingid,
#             attendee,
#             meeting,
#             attendance_status,
#             attendance_comments,
#             )
            
#             att_record.save()
                  
#             return render(request, "add_attendance.html", {'msg':'Attendance has been added','custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})
#         except: 
#             return render(request, "add_attendance.html", {'msg':'Error: Provide all information to create Attendance Record','custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all() })
#     return render(request, "add_attendance.html", {'custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all() })

def add_attendance(request):
    if request.method == "POST":
       form = AttendanceForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, "Attendance record has been added Successfully.")
           return render(request, "add_attendance.html",{'form':form,'custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})
       else:
           messages.success(request, ('There was an error in your form! Please try again...'))
           return render(request, 'add_attendance.html', {'form':form})
    else:
        form = AttendanceForm()
        return render(request, "add_attendance.html", {'form':form,'msg':'','custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})

# def add_attendance(request):
#     if request.method == "POST":
       
#         form = AttendanceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Attendance record has been added Successfully.")
#         return render(request, "add_attendance.html",{'form':form,'chair_by':Staff.objects.all()})
    
#     else:
#         form = AttendanceForm()
#         return render(request, "add_meeting.html", {'form':form,'chair_by':Staff.objects.all(),'msg':''})

def attendance_read(request):
    context = {'attendance_read':Attendance.objects.all()}
    return render(request, "attendance_read.html",context)

def add_penalty(request):
    if request.method == "POST":
       form = PenaltyForm(request.POST)
       if form.is_valid():
           form.save()
           messages.success(request, ('Penalty record has been submitted Successfully!'))
           return render(request, 'add_penalty.html', {'form':form})
       else:
           messages.success(request, ('There was an error in your form! Please try again...'))
           return render(request, 'add_penalty.html', {'form':form})
    else:
        form = PenaltyForm()
        return render(request, "add_penalty.html", {'form':form})


# 
def penalty_read(request):
    context = {'penalty_read':Penalty.objects.all()}
    return render(request, "penalty_read.html",context)

# def add_decision(request):
#     return render(request, 'add_decision.html')
# def decision_read(request):
#     return render(request, 'decision_read.html')

# def add_decision(request):
#     if request.method == "POST":
#         try:
#             offender_student = request.POST['offender_student']
            
#             penaltys = request.POST['penaltys']
            
#             complains = request.POST['complains']
                       
#             # meeting = Meeting.objects.get(meeting=meeting)
#             meeting = request.POST['meeting']
            
#             decision_comments = request.POST['decision_comments']
                        
#             Decision.objects.create(
#             offender_student=offender_student,
#             penaltys = penaltys,
#             complains = complains,
#             meeting=meeting,
#             decision_comments = decision_comments,
#             )
#             return render(request, "add_decision.html", {'msg':'Decision record has been added','offender_students':Student.objects.all(),'penaltys':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()})
#         except: 
#             return render(request, "add_decision.html", {'msg':'Please try again','offender_students':Student.objects.all(),'penaltys':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()})
#     return render(request, "add_decision.html", {'offender_students':Student.objects.all(),'penaltys':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all() })

def add_decision(request):
    if request.method == "POST":
            form = DecisionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Decision record has been added Successfully.")
                return render(request, "add_decision.html",{'form':form,'msg':'Decision record has been added','offender_students':Student.objects.all(),'penalties':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()})
            else:
                messages.success(request, ('There was an error in your form! Please try again...'))
            return render(request, 'add_decision.html', {'form':form})
    else:
        form = DecisionForm()
        return render(request, "add_decision.html", {'form':form,'msg':'','offender_students':Student.objects.all(),'penalties':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()})
    
def decision_read(request):
    context = {'decision_read':Decision.objects.all()}
    return render(request, "decision_read.html",context)

# pass id attribute from urls

def student_detail(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["student_data"] = Student.objects.get(id = id)
         
    return render(request, "student_detail.html", context)

# This Function will Delete the Student record
def student_delete(request, id):
        if request.method == 'POST':
            student = Student.objects.get(pk=id)
            person_id = student.person_ptr_id
            person = Person.objects.get(id=person_id)
            student.delete()
            person.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Student record has been deleted.')
        response = redirect('/student_read/')
        return response
    
def staff_delete(request, id):
        if request.method == 'POST':
            staff = Staff.objects.get(pk=id)
            person_id = staff.person_ptr_id
            person = Person.objects.get(id=person_id)
            staff.delete()
            person.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Staff record has been deleted.')
        response = redirect('/staff_read/')
        return response
    
def facultymember_delete(request, id):
        if request.method == 'POST':
            facultymember = FacultyMember.objects.get(pk=id)
            person_id = facultymember.person_ptr_id
            person = Person.objects.get(id=person_id)
            facultymember.delete()
            person.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Faculty Member record has been deleted.')
        response = redirect('/facultymember_read/')
        return response

# This Function will Delete the Faculty record
def faculty_delete(request, id):
        if request.method == 'POST':
            faculty = Faculty.objects.get(pk=id)
            faculty.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Faculty record has been deleted.')
        response = redirect('/faculty_read/')
        return response 
    
def term_delete(request, id):
        if request.method == 'POST':
            term = Term.objects.get(pk=id)
            term.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Term record has been deleted.')
        response = redirect('/term_read/')
        return response

# This Function will Delete the dept record    
def dept_delete(request, id):
        if request.method == 'POST':
            dept= Dept.objects.get(pk=id)
            dept.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Department record has been deleted.')
        response = redirect('/dept_read/')
        return response
    
# This Function will Delete the program record    
def program_delete(request, id):
        if request.method == 'POST':
            program= Program.objects.get(pk=id)
            program.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Program record has been deleted.')
        response = redirect('/program_read/')
        return response
    
# This Function will Delete the Offence record    
def offence_delete(request, id):
        if request.method == 'POST':
            offence= Offence.objects.get(pk=id)
            offence.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Offence record has been deleted.')
        response = redirect('/offence_read/')
        return response
        
# This Function will Delete the Complain record    
def complain_delete(request, id):
        if request.method == 'POST':
            complain= Complain.objects.get(pk=id)
            complain.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Complain record has been deleted.')
        response = redirect('/complain_read/')
        return response

# This Function will Delete the Meeting record    
def meeting_delete(request, id):
        if request.method == 'POST':
            meeting= Meeting.objects.get(pk=id)
            meeting.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Meeting record has been deleted.')
        response = redirect('/meeting_read/')
        return response

# This Function will Delete the Attendance record    
def attendance_delete(request, id):
        if request.method == 'POST':
            attendance= Attendance.objects.get(pk=id)
            attendance.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Attendance record has been deleted.')
        response = redirect('/attendance_read/')
        return response
    
# This Function will Delete the Penalty record    
def penalty_delete(request, id):
        if request.method == 'POST':
            penalty= Penalty.objects.get(pk=id)
            penalty.delete()
            # return HttpResponseRedirect('/')
        messages.warning(request, 'Penalty record has been deleted.')
        response = redirect('/penalty_read/')
        return response
    
def program_delete(request, id):
        if request.method == 'POST':
            program= Program.objects.get(pk=id)
            program.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Program record has been deleted.')
        response = redirect('/program_read/')
        return response
    
# This Function will Delete the Decision record    
def decision_delete(request, id):
        if request.method == 'POST':
            decision= Decision.objects.get(pk=id)
            decision.delete()
        # return HttpResponseRedirect('/')
        messages.warning(request, 'Decision record has been deleted.')
        response = redirect('/decision_read/')
        return response    
    

def offence_edit(request, id):
    offence_data =Offence.objects.get(pk=id)
    if request.method == "POST":
        offence_name = request.POST['offence_name']
        offence_comments = request.POST['offence_comments']
        offence_data = Offence.objects.filter(id).update(offence_name=offence_name,offence_comments=offence_comments)
        messages.success(request, "Offence Updated successfully")
        return redirect('offence_read')
    return render(request, 'offence_edit.html', {'offence_data':offence_data})

# def penalty_edit(request, id):
#     penalty_data =Offence.objects.get(pk=id)
#     if request.method == "POST":
#         offence_name = request.POST['offence_name']
#         offence_comments = request.POST['offence_comments']
#         offence_data = Offence.objects.filter(id).update(offence_name=offence_name,offence_comments=offence_comments)
#         messages.success(request, "Offence Updated successfully")
#         return redirect('offence_read')
#     return render(request, 'offence_edit.html', {'offence_data':offence_data})

# def faculty_edit(request, id):
#     faculty_data =Faculty.objects.get(pk=id)
#     if request.method == "POST":
#         faculty_name = request.POST['faculty_name']
#         faculty_data = Faculty.objects.filter(id).update(faculty_name=faculty_name)
#         messages.success(request, "Faculty Updated successfully")
#         return redirect('faculty_read')
#     return render(request, 'faculty_edit.html', {'faculty_data':faculty_data})

def faculty_detail(request, id):  
    faculty_data = Faculty.objects.get(id=id)  
    return render(request,'faculty_detail.html', {'faculty_data':faculty_data}) 

def faculty_edit(request, id):  
    faculty_data = Faculty.objects.get(id=id)  
    return render(request,'faculty_edit.html', {'faculty_data':faculty_data})  

def faculty_update(request, id):
    faculty_data = Faculty.objects.get(id=id)
    form = FacultyForm(request.POST, instance = faculty_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Faculty Updated successfully")  
        return redirect("faculty_read")
    return render(request, 'faculty_edit.html', {'faculty_data': faculty_data})

def dept_detail(request, id):  
    dept_data = Dept.objects.get(id=id) 
    # faculty_members = FacultyMember.
    return render(request,'dept_detail.html', {'dept_data':dept_data})

def dept_edit(request, id):  
    dept_data = Dept.objects.get(id=id)
    # context = {'facultys':Faculty.objects.all(), 'dept_data':dept_data }
    return render(request,'dept_edit.html', {'facultys':Faculty.objects.all(), 'dept_data':dept_data })  

def dept_update(request, id):
    dept_data = Dept.objects.get(id=id)
    form = DeptForm(request.POST, instance = dept_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Department Updated successfully")  
        return redirect("dept_read")
    return render(request, 'dept_edit.html', {'dept_data': dept_data})

def term_edit(request, id):  
    term_data = Term.objects.get(id=id)
    start_date = term_data.term_start_date
    end_date = term_data.term_end_date
    print(term_data.term_start_date)
    print(term_data.term_end_date)
    return render(request,'term_edit.html', {'term_data':term_data,'start_date':start_date,'end_date':end_date })  

def term_update(request, id):
    term_data = Term.objects.get(id=id)
    form = TermForm(request.POST, instance = term_data)  
    # print(term_data.term_start_date)
    # print(term_data.term_end_date)
    # if (term_data.term_start_date == ""):
    #     term_data.term_start_date = start_date
        
    # if (term_data.term_end_date == ""):
    #     term_data.term_end_date = end_date
       
    # print(term_data.term_end_date)
    if form.is_valid():  
        form.save()
        messages.success(request, "Term Updated successfully")  
        return redirect("term_read")
    return render(request, 'term_edit.html', {'term_data': term_data})

def term_detail(request, id):  
    term_data = Term.objects.get(id=id) 
    return render(request,'term_detail.html', {'term_data':term_data})


def program_edit(request, id):  
    program_data = Program.objects.get(id=id)
    terms = Term.objects.all()
    # context = {'program_data':program_data }
    return render(request,'program_edit.html', {'program_data':program_data,'terms':terms })  

def program_update(request, id):
    program_data = Program.objects.get(id=id)
    form = ProgramForm(request.POST, instance = program_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Program Updated successfully")  
        return redirect("program_read")
    return render(request, 'program_edit.html', {'program_data': program_data})

def program_detail(request, id):  
    program_data = Program.objects.get(id=id) 
    return render(request,'program_detail.html', {'program_data':program_data})

def designation_detail(request, id):  
    designation_data = Designation.objects.get(id=id) 
    return render(request,'designation_detail.html', {'designation_data':designation_data})

def staff_detail(request, id):  
    staff_data = Staff.objects.get(id=id) 
    return render(request,'staff_detail.html', {'staff_data':staff_data})

def facultymember_detail(request, id):  
    facultymember_data = FacultyMember.objects.get(id=id) 
    return render(request,'facultymember_detail.html', {'facultymember_data':facultymember_data})

def offence_detail(request, id):  
    offence_data = Offence.objects.get(id=id) 
    return render(request,'offence_detail.html', {'offence_data':offence_data})

def penalty_detail(request, id):  
    penalty_data = Penalty.objects.get(id=id) 
    return render(request,'penalty_detail.html', {'penalty_data':penalty_data})

def meeting_detail(request, id):  
    meeting_data = Meeting.objects.get(id=id) 
    return render(request,'meeting_detail.html', {'meeting_data':meeting_data})

def complain_detail(request, id):  
    meeting_data = Meeting.objects.get(id=id) 
    return render(request,'meeting_detail.html', {'meeting_data':meeting_data})