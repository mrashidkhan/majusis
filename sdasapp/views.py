from multiprocessing import AuthenticationError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student,FacultyMember,Staff
from sdasapp import *
from django.contrib.auth.models import User
from django.views.generic import View
from datetime import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError

# For Reports
from django.http import FileResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse


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

# This view will delete the Desination record
def designation_delete(request, id):
    if request.method == 'POST':
        try:
            designation = get_object_or_404(Designation, pk=id)
            # designation = Designation.objects.get(pk=id)
            designation.delete()
            messages.warning(request, 'Designation record has been deleted.')
            response = redirect('/designation_read/')
            return response
        except IntegrityError:
            error_url = reverse('designation_read')
            messages.warning(request, 'Cannot delete Designation record as it has associated child records.')
            return redirect(error_url)
        

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

# def add_term(request):
#     if request.method == "POST":
#             form = TermForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Term record has been submitted Successfully ")
#                 return redirect('term_read')
#             else:
#                 messages.success(request, "There was an error in your form! Please try again...")
#                 return redirect('add_term')
            
#             messages.success(request, "Term record has been submitted Successfully ")
#             return redirect(request, 'term_read')
#     else:
#         form = TermForm()
#         return render(request, "add_term.html", {'form':form})

def add_term(request):
    if request.method == "POST":
            form = TermForm(request.POST)
            if form.is_valid():
                term = form.save(commit=False)
                form.save()
                return redirect('term_read')
            
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

def student_edit(request, id):  
    student_data = Student.objects.get(id=id)
    terms = Term.objects.all()
    programs = Program.objects.all()
    
    context = {'student_data':student_data,'terms':terms,'programs':programs }
    return render(request,'student_edit.html', context) 

def student_update(request, id):
    student_data = Student.objects.get(id=id)
    terms = Term.objects.all()
    programs = Program.objects.all()
    form = StudentForm(request.POST, instance = student_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Student updated successfully")  
        return redirect("student_read")
    else:
        messages.success(request, "Student didn't update successfully") 
        terms = Term.objects.all()
        programs = Program.objects.all()
        context = {'student_data': student_data, 'terms':terms, 'programs':programs}
        return render(request, 'student_edit.html', context)

def add_staff(request):
    context = {}
    if request.method == "POST":
        # try:
            # dept_id = request.POST.get("depts")
            # depts = Dept.objects.get(id=dept_id)
            
                        
            designation_id = request.POST.get("designation")
            designation = Designation.objects.get(id=designation_id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_type = 'Staff'
            email_id = request.POST['email_id']
            contact_no = request.POST['contact_no']
            gender = request.POST['gender']
                                
            staff_user = Staff(
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                user_type=user_type,
                contact_no=contact_no,
                gender=gender,
                # depts=depts,
                designation=designation)
            
            staff_user.save()
            
            dept_list = request.POST.getlist("depts")
            for x in dept_list:
	            staff_user.depts.add(Dept.objects.get(id=x))
            
            messages.success(request, "Staff record has been added Successfully.")
            context = {'depts':Dept.objects.all(), 'designations':Designation.objects.all() }
            return render(request, "add_staff.html", context)
        
        # except: 
            messages.success(request, "Entered record information has problem")
            return render(request, "add_staff.html", context)
    else:
        context = {'depts':Dept.objects.all(), 'designations':Designation.objects.all() }
        return render(request, "add_staff.html", context)
        
        
# def add_staff(request):
#     # initial_data = {
#     #     'user_type' : 'Staff'
#     # }
#     if request.method == "POST":
#             form = StaffForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Staff record has been submitted Successfully ")
#             else:
#                 messages.success(request, "There was an error in your form! Please try again...")
#             return redirect('add_staff')
            
#             messages.success(request, "Staff record has been submitted Successfully ")
#             return redirect(request, 'staff_read')
#     else:
#         # initial=initial_data
#         form = StaffForm()
#         return render(request, "add_staff.html", {'form':form})        
    
def staff_read(request):
    context = {'staff_read':Staff.objects.all()}
    return render(request, "staff_read.html",context)

def add_facultymember(request):
    context = {}
    if request.method == "POST":
        # try:
            # dept_id = request.POST.get("depts")
            # depts = Dept.objects.get(id=dept_id)
            
                        
            designation_id = request.POST.get("designation")
            designation = Designation.objects.get(id=designation_id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_type = 'facultyMember'
            email_id = request.POST['email_id']
            contact_no = request.POST['contact_no']
            gender = request.POST['gender']
                                
            FacultyMember_user = FacultyMember(
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                user_type=user_type,
                contact_no=contact_no,
                gender=gender,
                # depts=depts,
                designation=designation)
            
            FacultyMember_user.save()
            
            dept_list = request.POST.getlist("depts")
            for x in dept_list:
	            FacultyMember_user.depts.add(Dept.objects.get(id=x))
            
            messages.success(request, "Faculty Member record has been added Successfully.")
            context = {'depts':Dept.objects.all(), 'designations':Designation.objects.all() }
            return render(request, "add_facultymember.html", context)
        
        # except: 
            messages.success(request, "Entered record information has problem")
            return render(request, "add_facultymember.html", context)
    else:
        context = {'depts':Dept.objects.all(), 'designations':Designation.objects.all() }
        return render(request, "add_facultymember.html", context)

# def add_facultymember(request):
#     initial_data = {
#         'user_type' : 'FacultyMember'
#     }
#     if request.method == "POST":
#             form = FacultyMemberForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Faculty member record has been submitted Successfully ")
#                 return redirect('add_facultymember')
#             else:
#                 messages.success(request, "There was an error in your form! Please try again...")
#                 return redirect('facultymember_read')
            
#             # messages.success(request, "Faculty Member record has been submitted Successfully ")
            
#     else:
#         form = FacultyMemberForm(initial=initial_data)
#         return render(request, "add_facultymember.html", {'form':form})        
    
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
    complainants = Person.objects.all()
    
    offences = Offence.objects.all()
    
                                          
    if request.method == "POST":
        try:
                        
            complain_date  = request.POST.get("complain_date")
            incident_date  = request.POST.get("incident_date")
            
            # updated_at = datetime.today()
            if complain_date < incident_date:
                messages.success(request, "Incident Date should be less than Complain Date")
                raise Exception('Incident Date should be less than Complain Date')
                # alert("Incident Date should be less than Complain Date")
                #  alert("Incident Date should be less than Complain Date")
            
            # updated_at = datetime.today()
            # if updated_at < complain_date:
            #     alert("Complain Date should be less than Today")
            
            complain_detail  = request.POST.get("complain_detail")                           
            
            complainant_id  = request.POST.get("complainants")
            complainant = Person.objects.get(id=complainant_id)
           
            complain_registered = Complain.objects.create(
            complain_date=complain_date,
            incident_date=incident_date,
            complain_detail=complain_detail,
            complainant = complainant, 
            )
            
            
            
            offender_list = request.POST.getlist("offenders")
            for x in offender_list:
                if x == complainant:
                    raise complainantequaloffender("Complainant and offender can't be same")
                else:
                    complain_registered.offenders.add(Student.objects.get(id=x))
            
            offence_list = request.POST.getlist("offences")
            for x in offence_list:
	            complain_registered.offences.add(Offence.objects.get(id=x))
            messages.success(request, "Complain record has been added Successfully.")
            offenders = Student.objects.all()
            complainants = Person.objects.all()
            offences = Offence.objects.all()
            
            context = {'complainants':complainants,'offenders':offenders,'offences':offences}
            return render(request, "add_complain.html", context)
        
        # except complainantequaloffender:
        #     message.error(request, "Complainant and offender should not be same")
        except:
            messages.error(request, "Failed to insert the record. Provide all required information ")
            offenders = Student.objects.all()
            complainants = Person.objects.all()
            offences = Offence.objects.all()
            context = {'msg':'Error: Provide all information to create Complain','complainants':complainants,'offenders':offenders,'offences':offences}
            return render(request, "add_complain.html", context)

    context = {'complainants':complainants,'offenders':offenders,'offences':offences}
    return render(request, "add_complain.html", context)
        

def search_student(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Student.objects.filter(student_id__icontains=q)  
    else:
        data= Data.objects.all()
    context = {'data':data}
    return render(request, "add_complain.html", context ) 
        


      
def complain_read(request):
    
    
    complain_read = Complain.objects.all()
    
    page = request.GET.get('page', 1)

    paginator = Paginator(complain_read,160)
    try:
        complain_read = paginator.page(page)
    except PageNotAnInteger:
        complain_read = paginator.page(1)
    except EmptyPage:
        complain_read = paginator.page(paginator.num_pages)

       
    context = {'complain_read':complain_read,'students':Student.objects.all()}
    return render(request, "complain_read.html",context)

# def add_meeting(request):
#     return render(request, 'add_meeting.html')

def complain_edit(request, id):
    complain_data = Complain.objects.get(pk=id)
    complain_offenders = complain_data.offenders.all()
    complain_offences = complain_data.offences.all()
    complain_date = complain_data.complain_date.strftime("%m/%d/%Y")
    incident_date = complain_data.incident_date.strftime("%m/%d/%Y")
    offenders = Student.objects.all()
    complainants = Student.objects.all()
    offences = Offence.objects.all()
    students = list(set(offenders)- set(complain_offenders))
    offences_notincluded = list(set(offences)- set(complain_offences))
    
    context = {'complain_data':complain_data,'offenders':offenders,'offences':offences,'complainants':complainants,'complain_date':complain_date,'incident_date':incident_date,'students':students,'offences_notincluded':offences_notincluded}
    return render(request, 'complain_edit.html', context)

def complain_update(request, id):
    complain_data = Complain.objects.get(pk=id)
    complain_date = complain_data.complain_date.strftime("%m/%d/%Y")
    incident_date = complain_data.incident_date.strftime("%m/%d/%Y")
    
    form = ComplainForm(request.POST, instance = complain_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Complain Updated successfully")  
        return redirect("complain_read")
    else:
        messages.success(request, "Complain didn't Update successfully")
        offenders = Student.objects.all()
        offences = Offence.objects.all()
        complainants = Student.objects.all()
        context = {'complain_data':complain_data,'offenders':offenders,'offences':offences,'complainants':complainants,'complain_date':complain_date,'incident_date':incident,'students':students,'offences_notincluded':offences_notincluded}
        return render(request, 'complain_edit.html', context)
    

def add_meeting(request):
    chair_by_list = Person.objects.exclude(user_type='Student')
    complains = Complain.objects.filter(complain_completed=False,meeting_assigned = False)
    context = {'chair_by_list':chair_by_list,'complains':complains}
    if request.method == "POST":
        # try:
            meeting_date = request.POST['meeting_date']
            meeting_location = request.POST['meeting_location']
            chairman = request.POST['chair_by']
            chair_by = Person.objects.get(id=chairman)
            comments = request.POST['comments']
            
            meeting_new = Meeting.objects.create(
            meeting_date=meeting_date,
            meeting_location=meeting_location,
            chair_by=chair_by,
            comments=comments,
            )
            complain_list = request.POST.getlist("complains")
            for x in complain_list:
                complain = Complain.objects.get(id=x)
                complain.meeting_assigned = 1
                # print(complain.meeting_assigned)
                complain.save()
                meeting_new.complains.add(complain)
                
                
            chair_by_list = Person.objects.exclude(user_type='Student')
            complains = Complain.objects.filter(complain_completed=False,meeting_assigned = False)
            context = {'chair_by_list':chair_by_list,'complains':complains,'msg':'Meeting has been added'}
            messages.warning(request, 'Meeting record has been added.')
            return render(request,"add_meeting.html", context)
        # except:
            chair_by_list = Person.objects.exclude(user_type='Student')
            complains = Complain.objects.filter(complain_completed=False,meeting_assigned = False)
            context = {'chair_by_list':chair_by_list,'complains':complains,'msg':'Error: Provide all information to create Meeting Record'}
            return render(request,"add_meeting.html", context)
            
    return render(request, "add_meeting.html", context)
       
# def add_meeting(request):
#     if request.method == "POST":
       
#         form = MeetingForm(request.POST)
#         if form.is_valid():
#             form.save()
            
#             messages.success(request, "Meeting record has been added Successfully.")
#         return render(request, "add_meeting.html",{'form':form,'chair_by':Staff.objects.all()})
#     # ,'msg':'Meeting has been added'
#     else:
#         form = MeetingForm()
#         return render(request, "add_meeting.html", {'form':form,'chair_by':Staff.objects.all(),'msg':''})
        
def meeting_read(request):
    context = {'meeting_read':Meeting.objects.all()}
    return render(request, "meeting_read.html",context)

def meeting_edit(request, id):
    
    meeting_data = Meeting.objects.get(pk=id)
    meeting_date = meeting_data.meeting_date.strftime("%m/%d/%Y")
    meeting_complains = meeting_data.complains.all()
    complains = Complain.objects.all()
    complains_nonincluded = list(set(complains)- set(meeting_complains))
    chair_by_list = Person.objects.exclude(user_type='Student')
        
    context = {'meeting_data':meeting_data,'complains':complains,'complains_nonincluded':complains_nonincluded,'meeting_date':meeting_date,'meeting_complains':meeting_complains,'chair_by_list':chair_by_list}
    return render(request, 'meeting_edit.html', context)

def meeting_update(request, id):
    meeting_data = Meeting.objects.get(pk=id)
    meeting_date = meeting_data.meeting_date.strftime("%m/%d/%Y")   
    form = MeetingForm(request.POST, instance = meeting_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Complain Updated successfully")  
        return redirect("meeting_read")
    else:
        messages.success(request, "Complain didn't Update successfully")
        meeting_data = Meeting.objects.get(pk=id)
        meeting_date = meeting_data.meeting_date.strftime("%m/%d/%Y")
        meeting_complains = meeting_data.complains.all()
        complains = Complain.objects.all()
        complains_nonincluded = list(set(complains)- set(meeting_complains))
        context = {'meeting_data':meeting_data,'complains':complains,'complains_nonincluded':complains_nonincluded,'meeting_date':meeting_date,'meeting_complains':meeting_complains,'chair_by_list':chair_by_list}
        return render(request, 'meeting_edit.html', context)
    
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


def add_attendance(request):
    faculty_attendees = FacultyMember.objects.all()
    staff_attendees = Staff.objects.all()
    # student_attendees = Student.objects.all()
    meetings = Meeting.objects.all()
    
    if request.method == "POST":
        # try:
            meeting_id = request.POST['meeting']
            complain_id = request.POST['complain']        
            # faculty_attendee = request.POST['faculty_attendee'] 
            # staff_attendee = request.POST['staff_attendee']
            # student_attendee = request.POST['student_attendee'] 
            # attendance_status = request.POST['attendance_status']
            # attendance_comments = request.POST['attendance_comments']
                       
            # attendance_record = Attendance.objects.create(
            # meeting = meeting,
            # complaint = complaint,
            # faculty_attendee = faculty_attendee,
            # staff_attendee = staff_attendee,
            # student_attendee = student_attendee,
            # attendance_status = attendance_status,
            # attendance_comments = attendance_comments,
            # )
            
            faculty_attendees = request.POST.getlist("faculty_attendees")
            for faculty_attendee in faculty_attendees:
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                faculty_attendee = Person.objects.get(id=faculty_attendee)
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = faculty_attendee,
                attendance_status = "Present",
                comments = "Faculty Member",
            )
            
            staff_attendees = request.POST.getlist("staff_attendees")
            for staff_attendee in staff_attendees:
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                staff_attendee = Person.objects.get(id=staff_attendee)
                
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = staff_attendee,
                attendance_status = "Present",
                comments = "Staff",
            )
            
            
            offender_attendees_present = request.POST.getlist("offenders")
            present_offenders = list(offender_attendees_present)
            
            # present_offenders_int =int(present_offenders)
            
            
            offenders_present = []
            for present in present_offenders:
                offenders_present.append(int(present))
                print(int(present ))
                
            print(offenders_present)
            
            for offender_present in offenders_present:
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                offender = Student.objects.get(id=offender_present)
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = offender,
                attendance_status = "Present",
                comments = "Offender",
            )
            
            
            
            # offender_attendees_absent = complain.offenders.exclude(offenders_all)
            
            
            # non_sel_offender = request.POST.getlist("non_sel_offender")
            # print(non_sel_offender)
            # offenders_present = []
            
            # for element in offender_attendees_present:
            #     offenders_present.append(element.id)
            # print(offender_attendees_present)
            # offenders_present = []
            offenders_all_instances = complain.offenders.all()
            offenders_all = []
            for element in offenders_all_instances:
                offenders_all.append(element.id)
              
            # offender_attendees_absent = list(set(offenders_all)- set(offender_attendees_present))
            
            # offender_attendees_absent = []
            # for element in offenders_all:
            #     if element not in offender_attendees_present:
            #         offender_attendees_absent.append(element)
            
            s = set(offenders_present)
            print("all presents")
            print(s)
            offender_attendees_absent = [x for x in offenders_all if x not in s]
            
            print("All Offenders")
            print(offenders_all)
            print("All Present Offenders")
            print(offender_attendees_present)
            print("All Absent Offenders")
            print(offender_attendees_absent)
            # for element in offenders_all_absent:
            #      temp.append(element.id)
                
            
            # offender_attendees_absent = []
            
            # for element in temp:
            #     if element not in offender_attendees_present:
            #         offender_attendees_absent.append(element)
            # print(offender_attendees_absent)  
            # offender_attendees_absent:      
            for offenderabsent in offender_attendees_absent:
                
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                
                offender_absent = Student.objects.get(id=offenderabsent)
                
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = offender_absent,
                attendance_status = "Absent",
                comments = "Offender",
            )
            
            complainant_attendee = request.POST['complainant']
            if (complainant_attendee):
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                complainant = Student.objects.get(id=complainant_attendee) 
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = complainant,
                attendance_status = "Present",
                comments = "Complainant",
                )
            else:
                meeting = Meeting.objects.get(id= meeting_id)
                complain = Complain.objects.get(id=complain_id)
                # complainant = meeting.complainant 
                Attendance.objects.create(
                meeting = meeting,
                complain = complain,
                attendee = complain.complainant,
                attendance_status = "Absent",
                comments = "Complainant",
                )
                
                    
            # attendance_record.save()
            complain.attendance_done = 1 
            complain.save()      
            return render(request, "add_attendance.html", {'msg':'Attendance has been added','custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})
        # except:
            faculty_attendees = FacultyMember.objects.all()
            staff_attendees = Staff.objects.all()
            meetings = Meeting.objects.all()
            context = {'msg':'Error: Provide all information to create Attendance Record','meetings':meetings,'faculty_attendees':faculty_attendees,'staff_attendees':staff_attendees}
            return render(request, "add_attendance.html", context)
    # context = {'faculty_attendees':faculty_attendees, 'staff_attendees':staff_attendees, 'students_attendees':student_attendees,'meetings':meetings}
    context = {'meetings':meetings,'faculty_attendees':faculty_attendees,'staff_attendees':staff_attendees}
    return render(request, "add_attendance.html", context)



# def add_attendance(request):
#     if request.method == "POST":
#        form = AttendanceForm(request.POST)
#        if form.is_valid():
#            form.save()
#            messages.success(request, "Attendance record has been added Successfully.")
#            return render(request, "add_attendance.html",{'form':form,'custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})
#        else:
#            messages.success(request, ('There was an error in your form! Please try again...'))
#            return render(request, 'add_attendance.html', {'form':form})
#     else:
#         form = AttendanceForm()
#         return render(request, "add_attendance.html", {'form':form,'msg':'','custom_users':CustomUser.objects.all(),'meetings':Meeting.objects.all()})

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

def add_decision(request):
    if request.method == "POST":
        # try:
            # offender_student_id = request.POST['offender']
            # offender_student = Student.objects.get(id=offender_student_id)
                        
            complain_id = request.POST['complain']
            complain = Complain.objects.get(id=complain_id)           
            
            meeting_id = request.POST['meeting']
            meeting = Meeting.objects.get(id= meeting_id)
            
            # comments = request.POST['decision_comments']
            offenders = complain.offenders.all()
            for offender in offenders:
                
                decision_registered = Decision.objects.create(
                offender_student=offender,
                complain = complain,
                meeting=meeting,
                )
                penaltyid = str(offender.id)
                id = "penalty_" + penaltyid
                penalty_list = request.POST.getlist(id)
                for x in penalty_list:
	                decision_registered.penalties.add(Penalty.objects.get(id=x))
            
            complain_id = request.POST['complain']
            print(complain_id)
            complain = Complain.objects.get(id=complain_id)
            print(complain)
            complain.complain_completed = True
            complain.save()
            print(complain.complain_completed)
            meetings = Meeting.objects.all()
            # complains = Complain.objects.filter(complain_completed=0)
            # complains = Complain.objects.all()
            # offender_students = Student.objects.all()
            # penalties = Penalty.objects.all()
            # context = {'meetings':meetings,'offender_students':offender_students,'penalties':penalties,'complains':complains}
            
            # print(complain.complain_completed)
            context = {'meetings':meetings}
            messages.success(request, ('Decision record has been submitted Successfully!'))
            return render(request, "add_decision.html", context)
        # except:
            meetings = Meeting.objects.all()
            # complains = Complain.objects.filter(complain_completed=0)
            # complains = Complain.objects.all()
            # offender_students = Student.objects.all()
            # penalties = Penalty.objects.all()
            # context = {'meetings':meetings,'offender_students':offender_students,'penalties':penalties,'complains':complains}
            context = {'msg':'Please try again','meetings':meetings}
            messages.error(request, ('There is error in the information!'))
            return render(request, "add_decision.html", context)
    
    meetings = Meeting.objects.all()
    # complains = Complain.objects.filter(complain_completed=0)
    # complains = Complain.objects.all()
    # offender_students = Student.objects.all()
    # penalties = Penalty.objects.all()
    # context = {'meetings':meetings,'offender_students':offender_students,'penalties':penalties,'complains':complains}
    context = {'meetings':meetings}
    return render(request, "add_decision.html", context )

# def add_decision(request):
#     if request.method == "POST":
#             form = DecisionForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Decision record has been added Successfully.")
#                 return render(request, "add_decision.html",{'form':form,'msg':'Decision record has been added','offender_students':Student.objects.all(),'penalties':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()})
#             else:
#                 messages.success(request, ('There was an error in your form! Please try again...'))
#             return render(request, 'add_decision.html', {'form':form})
#     else:
#         form = DecisionForm()
#         complains = Complain.objects.filter(complain_completed=0)

#         context = 'offender_students':Student.objects.all(),'penalties':Penalty.objects.all(),'complains':Complain.objects.all(),'meetings':Meeting.objects.all()}
#         return render(request, "add_decision.html", {'form':form,'msg':'',context)
    
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
        try:
            student = get_object_or_404(Student, pk=id)
            # student = Student.objects.get(pk=id)
            person_id = student.person_ptr_id
            person = Person.objects.get(id=person_id)
            student.delete()
            person.delete()
            messages.warning(request, 'Student record has been deleted.')
            response = redirect('/student_read/')
            return response
        except IntegrityError:
            error_url = reverse('student_read')
            messages.warning(request, 'Cannot delete Student record as it has associated child records.')
            return redirect(error_url)
    
def staff_delete(request, id):
    if request.method == 'POST':
        try:
            staff = get_object_or_404(Staff, pk=id)
            # staff = Staff.objects.get(pk=id)
            person_id = staff.person_ptr_id
            person = Person.objects.get(id=person_id)
            staff.delete()
            person.delete()
            messages.warning(request, 'Staff record has been deleted.')
            response = redirect('/staff_read/')
            return response
        except IntegrityError:
            error_url = reverse('staff_read')
            messages.warning(request, 'Cannot delete Staff record as it has associated child records.')
            return redirect(error_url)
        
    
def facultymember_delete(request, id):
    facultymember = get_object_or_404(FacultyMember, pk=id)
    person = facultymember.person_ptr

    if request.method == 'POST':
        try:
            associated_facultymembers = FacultyMember.objects.filter(person_ptr=person).exclude(pk=id)
            if associated_facultymembers.exists():
                # Don't delete associated Person if it has other associated FacultyMember objects
                messages.warning(request, 'Cannot delete faculty member record as the associated person has other associated faculty member records.')
                return redirect('facultymember_read', id=id)
            else:
                facultymember.delete()
                person.delete()
                messages.success(request, 'Faculty member record has been deleted.')
                return redirect('facultymember_read')
        except IntegrityError:
            error_url = reverse('facultymember_read')
            messages.warning(request, 'Cannot delete faculty member record as it has associated child records.')
            return redirect(error_url)

# This Function will Delete the Faculty record
def faculty_delete(request, id):
    faculty = get_object_or_404(Faculty, pk=id)
    if request.method == 'POST':
        try:
            faculty.delete()
            messages.warning(request, 'Faculty record has been deleted.')
            response = redirect('/faculty_read/')
            return response
        except IntegrityError:
            error_url = reverse('faculty_read')
            messages.warning(request, 'Cannot delete Faculty record as it has associated child records.')
            return redirect(error_url)
            
    
def term_delete(request, id):
        if request.method == 'POST':
            try:
                term = get_object_or_404(Term, pk=id)
                term.delete()
                messages.warning(request, 'Term record has been deleted.')
                response = redirect('/term_read/')
                return response
            except IntegrityError:
                error_url = reverse('term_read')
                messages.warning(request, 'Cannot delete Term record as it has associated child records.')
                return redirect(error_url)

# This Function will Delete the dept record    
def dept_delete(request, id):
    if request.method == 'POST':
        try:
            dept = get_object_or_404(Dept, pk=id)
            # dept= Dept.objects.get(pk=id)
            dept.delete()
            messages.warning(request, 'Department record has been deleted.')
            response = redirect('/dept_read/')
            return response
        except IntegrityError:
            error_url = reverse('dept_read')
            messages.warning(request, 'Cannot delete Dept record as it has associated child records.')
            return redirect(error_url)
            
    
# This Function will Delete the program record    
def program_delete(request, id):
    if request.method == 'POST':
        try:
            program = get_object_or_404(Program, pk=id)
            # program= Program.objects.get(pk=id)
            program.delete()
            messages.warning(request, 'Program record has been deleted.')
            response = redirect('/program_read/')
            return response
        except IntegrityError:
            error_url = reverse('program_read')
            messages.warning(request, 'Cannot delete Program record as it has associated child records.')
            return redirect(error_url)
    
# This Function will Delete the Offence record    
def offence_delete(request, id):
    if request.method == 'POST':
        try:
            # offence= Offence.objects.get(pk=id)
            offence = get_object_or_404(Offence, pk=id)
            offence.delete()
            messages.warning(request, 'Offence record has been deleted.')
            response = redirect('/offence_read/')
            return response
        except IntegrityError:
            error_url = reverse('offence_read')
            messages.warning(request, 'Cannot delete Offence record as it has associated child records.')
            return redirect(error_url)
        
# This Function will Delete the Complain record    
def complain_delete(request, id):
    if request.method == 'POST':
        try:
            # complain= Complain.objects.get(pk=id)
            complain = get_object_or_404(Complain, pk=id)
            complain.delete()
            messages.warning(request, 'Complain record has been deleted.')
            response = redirect('/complain_read/')
            return response
        except IntegrityError:
            error_url = reverse('complain_read')
            messages.warning(request, 'Cannot delete Complaint record as it has associated child records.')
            return redirect(error_url)

# This Function will Delete the Meeting record    
def meeting_delete(request, id):
    if request.method == 'POST':
        try:
            meeting = get_object_or_404(Meeting, pk=id)
            # meeting= Meeting.objects.get(pk=id)
            meeting.delete()
            messages.warning(request, 'Meeting record has been deleted.')
            response = redirect('/meeting_read/')
            return response
        except IntegrityError:
            error_url = reverse('meeting_read')
            messages.warning(request, 'Cannot delete Meeting record as it has associated child records.')
            return redirect(error_url)

# This Function will Delete the Attendance record    
def attendance_delete(request, id):
    if request.method == 'POST':
        try:
            # attendance= Attendance.objects.get(pk=id)
            attendance = get_object_or_404(Attendance, pk=id)
            attendance.delete()
            messages.warning(request, 'Attendance record has been deleted.')
            response = redirect('/attendance_read/')
            return response
        except IntegrityError:
            error_url = reverse('attendance_read')
            messages.warning(request, 'Cannot delete Attendance record as it has associated child records.')
            return redirect(error_url)
    
# This Function will Delete the Penalty record    
def penalty_delete(request, id):
    if request.method == 'POST':
        try:
            penalty = get_object_or_404(Penalty, pk=id)
            # penalty= Penalty.objects.get(pk=id)
            penalty.delete()
            messages.warning(request, 'Penalty record has been deleted.')
            response = redirect('/penalty_read/')
            return response
        except IntegrityError:
            error_url = reverse('penalty_read')
            messages.warning(request, 'Cannot delete Penalty record as it has associated child records.')
            return redirect(error_url)
    
# This Function will Delete the Decision record 
def decision_delete(request, id):
    if request.method == 'POST':
        try:
            decision = get_object_or_404(Decision, pk=id)
            # decision= Decision.objects.get(pk=id)
            decision.delete()
            messages.warning(request, 'Decision record has been deleted.')
            response = redirect('/decision_read/')
            return response
        except IntegrityError:
            error_url = reverse('decision_read')
            messages.warning(request, 'Cannot delete Decision record as it has associated child records.')
            return redirect(error_url)   
    

def offence_edit(request, id):
    offence_data =Offence.objects.get(pk=id)
    # if request.method == "POST":
    #     offence_name = request.POST['offence_name']
    #     offence_comments = request.POST['offence_comments']
    #     offence_data = Offence.objects.filter(id).update(offence_name=offence_name,offence_comments=offence_comments)
    #     messages.success(request, "Offence Updated successfully")
    #     return redirect('offence_read')
    return render(request, 'offence_edit.html', {'offence_data':offence_data})

def offence_update(request, id):
    offence_data = Offence.objects.get(id=id)
    print(offence_data)
    form = OffenceForm(request.POST, instance = offence_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Offence Updated successfully")  
        return redirect("offence_read")
    else:
        messages.success(request, "Offence didn't Update successfully") 
    return render(request, 'offence_edit.html', {'offence_data': offence_data})

def penalty_edit(request, id):
    penalty_data = Penalty.objects.get(pk=id)
    # if request.method == "POST":
    #     offence_name = request.POST['offence_name']
    #     offence_comments = request.POST['offence_comments']
    #     offence_data = Offence.objects.filter(id).update(offence_name=offence_name,offence_comments=offence_comments)
    #     messages.success(request, "Offence Updated successfully")
    #     return redirect('offence_read')
    return render(request, 'penalty_edit.html', {'penalty_data':penalty_data})

def penalty_update(request, id):
    penalty_data = Penalty.objects.get(id=id)
    form = PenaltyForm(request.POST, instance = penalty_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Penalty Updated successfully")  
        return redirect("penalty_read")
    else:
        messages.success(request, "Penalty didn't Update successfully") 
        return render(request, 'penalty_edit.html', {'penalty_data': penalty_data})

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
    term_name = term_data.term_name
    term_start_date = term_data.term_start_date
    term_end_date = term_data.term_end_date
    term_comments = term_data.term_comments
    # term_start_date = start_date.strftime("%m/%d/%Y")
    print(term_start_date)
    # end_date = term_data.term_end_date
    # term_end_date = end_date.strftime("%m-%d-%Y")
    print(term_end_date)
    # context = {'term_data':term_data,'term_start_date':term_start_date,'term_end_date':term_end_date }
    context = {'term_data':term_data,'term_start_date':term_start_date,'term_end_date':term_end_date,'term_comments':term_comments}
    return render(request,'term_edit.html', context )  

    
 

def term_update(request, id):
    term_data = Term.objects.get(id=id)
    start_date = term_data.term_start_date
    term_start_date = start_date.strftime("%m/%d/%Y")
    end_date = term_data.term_end_date
    term_end_date = end_date.strftime("%m/%d/%Y")
    term_comments = term_data.comments
    form = TermForm(request.POST, instance = term_data)  
    print(term_start_date)
    print(term_end_date)
    # if (term_data.term_start_date == ""):
    #     term_data.term_start_date = start_date
        
    # if (term_data.term_end_date == ""):
    #     term_data.term_end_date = end_date
       
    # print(term_data.term_end_date)
    if form.is_valid():  
        form.save()
        
        messages.success(request, "Term Updated successfully")  
        return redirect("term_read")
    context = {'term_data':term_data,'term_start_date':term_start_date,'term_end_date':term_end_date,'term_comments':term_comments}
    return render(request, 'term_edit.html', context)

# def term_update(request, id):  
#     term_data = Term.objects.get(id=id)
    
    
#     form = TermForm(request.POST, instance = term_data)
#     print(term_data.term_name)
#     print(term_data.term_start_date)
#     print(term_data.term_end_date)
#     print(term_data.comments)
    
#     if form.is_valid():  
#         form.save()
#         messages.success(request, "Term Updated successfully")  
#         return redirect("term_read") 
#     return render(request,'term_edit.html', {'term_data':term_data})

def term_detail(request, id):  
    term_data = Term.objects.get(id=id) 
    return render(request,'term_detail.html', {'term_data':term_data})


def program_edit(request, id):  
    program_data = Program.objects.get(id=id)
    terms = Term.objects.all()
    depts = Dept.objects.all()
    
    context = {'program_data':program_data,'terms':terms,'depts':depts }
    return render(request,'program_edit.html', context)  

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

def designation_edit(request, id):  
    designation_data = Designation.objects.get(id=id)
    context = {'designation_data':designation_data }
    return render(request,'designation_edit.html', context)

def designation_update(request, id):
    designation_data = Designation.objects.get(id=id)
    form = DesignationForm(request.POST, instance = designation_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Designation Updated successfully")  
        return redirect("designation_read")
    return render(request, 'designation_edit.html', {'designation_data': designation_data})

def staff_detail(request, id):  
    staff_data = Staff.objects.get(id=id)
    deptartments = Dept.objects.all()
    designations = Designation.objects.all()
    context = {'staff_data':staff_data,'designations':designations,'deptartments':deptartments}
    return render(request,'staff_detail.html', context)

def facultymember_detail(request, id):  
    facultymember_data = FacultyMember.objects.get(id=id)
    deptartments = Dept.objects.all()
    designations = Designation.objects.all()
    context = {'facultymember_data':facultymember_data,'designations':designations,'deptartments':deptartments}
    return render(request,'facultymember_detail.html', context)

def facultymember_edit(request, id):  
    facultymember_data = FacultyMember.objects.get(id=id) 
    deptartments = Dept.objects.all()
    designations = Designation.objects.all()
    context = {'facultymember_data':facultymember_data,'designations':designations,'deptartments':deptartments}
    return render(request,'facultymember_edit.html', context ) 

def staff_edit(request, id):  
    staff_data = Staff.objects.get(id=id) 
    departments = Dept.objects.all()
    designations = Designation.objects.all()
    context = {'staff_data':staff_data,'designations':designations,'departments':departments}
    return render(request,'staff_edit.html', context )  

def facultymember_update(request, id):
    facultymember_data = FacultyMember.objects.get(id=id)
    print(facultymember_data)
    form = FacultyMemberForm(request.POST, instance = facultymember_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Faculty Member Updated successfully")
        departments = Dept.objects.all()
        designations = Designation.objects.all()
        facultymember_data = FacultyMember.objects.get(id=id)
        context = {'facultymember_data':facultymember_data,'designations':designations,'departments':departments}   
        return redirect("facultymember_read")
    else:
        messages.success(request, "Faculty Member did not Update successfully")  
    return render(request, 'facultymember_edit.html', {'facultymember_data': facultymember_data})

def staff_update(request, id):
    staff_data = Staff.objects.get(id=id)
    print(staff_data)
    form = StaffForm(request.POST, instance = staff_data)  
    if form.is_valid():  
        form.save()
        messages.success(request, "Staff Member Updated successfully")
        staff_data = Staff.objects.get(id=id) 
     
        return redirect("staff_read")
    else:
        messages.success(request, "Staff Member did not Update successfully")
        departments = Dept.objects.all()
        designations = Designation.objects.all()
        staff_data = Staff.objects.get(id=id)
        context = {'staff_data':staff_data,'designations':designations,'departments':departments} 
    return render(request, 'staff_edit.html', context)

def offence_detail(request, id):  
    offence_data = Offence.objects.get(id=id) 
    return render(request,'offence_detail.html', {'offence_data':offence_data})

def penalty_detail(request, id):  
    penalty_data = Penalty.objects.get(id=id) 
    return render(request,'penalty_detail.html', {'penalty_data':penalty_data})

def meeting_detail(request, id):  
    meeting_data = Meeting.objects.get(id=id) 
    return render(request,'meeting_detail.html', {'meeting_data':meeting_data})

# def complain_detail(request, id):  
#     complain_data = Complain.objects.get(id=id) 
#     return render(request,'complain_detail.html', {'complain_data':complain_data})

def complain_detail(request, id):
    complain_data = Complain.objects.get(pk=id)
    complain_offenders = complain_data.offenders.all()
    complain_offences = complain_data.offences.all()
    complain_date = complain_data.complain_date.strftime("%m/%d/%Y")
    incident_date = complain_data.incident_date.strftime("%m/%d/%Y")
    offenders = Student.objects.all()
    complainants = Student.objects.all()
    offences = Offence.objects.all()
    students = list(set(offenders)- set(complain_offenders))
    offences_notincluded = list(set(offences)- set(complain_offences))
    
    context = {'complain_data':complain_data,'offenders':offenders,'offences':offences,'complainants':complainants,'complain_date':complain_date,'incident_date':incident_date,'students':students,'offences_notincluded':offences_notincluded}
    return render(request, 'complain_detail.html', context)

def load_complainants(request):
    complainant_type = request.GET.get('complainant_type')
    if complainant_type == "Student":
        complainants = Student.objects.all()
    else:
        complainants = Person.objects.filter(user_type=complainant_type).order_by('first_name')
    return render(request, 'complainants_dropdown_list_options.html', { 'complainants': complainants})

def ajax_complain_offenders(request):
    complainant = request.GET.get('complainant')
    print(complainant)
    offenders = Student.objects.exclude(id=complainant)
    # print()
    return render(request, 'offenders_dropdown_list_options.html', { 'offenders': offenders})

def load_students(request):
    complainant_type = request.GET.get('complainant_type')
    complainant = request.GET.get('complainant')
    print(complainant_type)
    print(complainant)

    offenders = Student.objects.exclude(id = complainant)
    return render(request, 'students_dropdown_list_options.html', { 'offenders': offenders})

# For Attendance Form

def ajax_attendance_meeting(request):
    meetingid = request.GET.get('meeting')
    meeting = Meeting.objects.get(id=meetingid)    
    
    complains = meeting.complains.filter(attendance_done=False)
    
    return render(request, 'ajax_attendance_meeting.html', { 'complains': complains})

def ajax_attendance_complainant(request):
    complainid = request.GET.get('complain')
    complain = Complain.objects.get(id=complainid)    
    # complain.complainant
    complainant_id = complain.complainant_id
    # print(complainant)
    complainant = Student.objects.get(id=complainant_id)
    
    context = {'complainant':complainant}
    return render(request, 'ajax_attendance_complainant.html', context)

def ajax_attendance_offenders(request):
    complainid = request.GET.get('complain')
    complain = Complain.objects.get(id=complainid)    
    
    offenders = complain.offenders.all()
    
    context = {'offenders':offenders}
    return render(request, 'ajax_attendance_offenders.html', context)


# For Decision Form

def ajax_decision_meeting(request):
    meetingid = request.GET.get('meeting')
    meeting = Meeting.objects.get(id=meetingid)    
    
    complains = meeting.complains.filter(complain_completed=False)
    
    return render(request, 'ajax_decision_meeting.html', { 'complains': complains})

def ajax_decision_complain(request):
    complainid = request.GET.get('complain')
    complain = Complain.objects.get(id=complainid)    
    # offenders = complain.offenders.filter(complain_completed=False)
    offenders = complain.offenders.all()
    # complainant = Student.objects.get(id=complainant_id)
    penalties = Penalty.objects.all()
    context = {'offenders':offenders,'penalties':penalties}
    return render(request, 'ajax_decision_complain.html', context)

# def ajax_decision_offenders(request):
#     complainid = request.GET.get('complain')
#     complain = Complain.objects.get(id=complainid)    
    
#     offenders = complain.offenders.all()
    
#     context = {'offenders':offenders}
#     return render(request, 'ajax_decision_offenders.html', context)

# def search(request):
#     query = request.GET.get('q')
#     if query:
#         authors = Student.objects.filter(Q(name='John') | Q(name='Jane'))
#         books = Book.objects.filter(authors__in=authors)
#     else:
#         offenders = []
#     return render(request, 'search_results.html', {'offenders': offenders})

# For Search complains against student
def search(request):
    query = request.GET.get('q')
    if query:
        offender = Student.objects.filter(Q(student_id=query))
        complains = Complain.objects.filter(offenders__in=offender)
    else:
        complains = []
    context ={'complains': complains,'query':query,'students':Student.objects.all()}
    return render(request, 'search_results.html', context)


# For Reports Designing

def generate_pdf(request, *args, **kwargs):
    template = get_template('pdf_template.html')
    context = {
        'students': Student.objects.all()
    }
    html = template.render(context)
    pdf_file = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_file)
    pdf_file.seek(0)
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'
    return response

def complain_report(request, *args, **kwargs):
    template = get_template('complain_report.html')
    context = {
        'complains': Complain.objects.all()
    }
    html = template.render(context)
    pdf_file = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_file)
    pdf_file.seek(0)
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="complain_report.pdf"'
    return response

def complain_id_report(request, pk):
    complain = get_object_or_404(Complain, pk=pk)
    html = render_to_string('complain_id_report.html', {'complain': complain})
    pdf_file = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_file)
    pdf_file.seek(0)
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="complain_id_report.pdf"'
    return response

def add_fyp(request):
    if request.method == 'POST':
        form = FYPForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('fyp_list')
    else:
        form = FYPForm()
    return render(request, 'add_fyp.html', {'form': form})