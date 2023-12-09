# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.utils import timezone

# from .views import *

from .models import CustomUser

class DatePickerInput(forms.DateInput):
   input_type = 'date'

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
        
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields ='__all__'
        
class DeptForm(forms.ModelForm):
    class Meta:
        model = Dept
        # fields ='__all__'
        fields = ['dept_name','dept_location','faculty'] 
        
        labels = {
            'dept_name': ('Department Name'),
            'dept_location': ('Department Location'),
            'faculty': ('Faculty'),
        }
        
        widgets = {
        'dept_name':forms.TextInput(attrs={'class':'form-control '}),
        'dept_location':forms.Select(attrs={'class':'form-control '}),
        'faculty':forms.Select(attrs={'class':'form-control '}),
        }

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['term_name', 'term_start_date', 'term_end_date', 'comments'] 
        
        labels = {
            'term_name': ('Term Name'),
            'term_start_date': ('Term Start Date'),
            'term_end_date': ('Term End Date'),
            'comments': ('Comments'),
        }
        
        # widgets = {
        #     'term_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'term_start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date', 'required': True}),
        #     'term_end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date', 'required': True}),
        #     'comments': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        widgets = {
            'term_name': forms.TextInput(attrs={'class': 'form-control'}),
            'term_start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
            'term_end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
            'comments': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            term_start_date_value = cleaned_data.get('term_start_date')
            term_end_date_value = cleaned_data.get('term_end_date')
            today = date.today()

            if term_start_date_value and term_end_date_value and term_start_date_value > term_end_date_value:
                raise forms.ValidationError("Term Start Date should be less than or equal to Term End Date.")

            if term_start_date_value and term_start_date_value < today:
                raise forms.ValidationError("Term Start Date cannot be in the Past.")

            if term_end_date_value and term_end_date_value < today:
                raise forms.ValidationError("Term End Date cannot be in the Past.")
                
            term_name = cleaned_data.get('term_name')
            if not re.match(r"^(SP|FA)\d{2}$", term_name):
                raise forms.ValidationError("Term Name should start with 'SP' or 'FA' followed by 2 digits between 20 and 29.")
                
            if Term.objects.filter(term_name=term_name).exists():
                raise forms.ValidationError("Term Name must be unique.")
                
     
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        # fields ='__all__'
        
        # program_code = forms.IntegerField(validators=[validate_code_length])
        
        fields = ['program_name','dept','program_type','term'] 
        
        labels = {
            'program_name': ('Program Name'),
            'program_type': ('Program Type'),
            'dept': ('Department'),
            'term': ('Term'),
            
        }
        
        widgets = {
        'program_name':forms.TextInput(attrs={'class':'form-control '}),
        'program_code':forms.TextInput(attrs={'class':'form-control '}),
        'program_type':forms.Select(attrs={'class':'form-control '}),
        'dept':forms.Select(attrs={'class':'form-control '}),
        'term':forms.Select(attrs={'class':'form-control '}),
        
         }
        

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id','first_name','last_name','email_id','contact_no','gender','term','program']
        exclude = ['user_type','meetings','facultymember_id']
        
        # fields ='__all__'
    #  'User.first_name', 'User.last_name',   

# AuthorFormSet = modelformset_factory(Author, form=AuthorForm)
# AuthorFormSet = modelformset_factory(Student, fields=('name', 'title'))

# class StaffForm(forms.ModelForm):
#     class Meta:
#         model = Staff
        
#         depts = forms.ModelMultipleChoiceField(
#                        widget = forms.CheckboxSelectMultiple,
#                        queryset = Dept.objects.all()
#                )
#         fields = ['first_name','last_name','email_id','designation','depts']
#         exclude = ['user_type','meetings','staff_id']
#         labels = {
#             'first_name': ('First Name'),
#             'last_name': ('Last Name'),
#             'email_id': ('Email'),
#             'designation': ('Designation'),
#             'depts':('Departments')
            
#         }
        
#         widgets = {
#         'first_name':forms.TextInput(attrs={'class':'form-control'}),
#         'last_name':forms.TextInput(attrs={'class':'form-control'}),
#         'email_id':forms.EmailInput(attrs={'class':'form-control'}),
#         'designation':forms.Select(attrs={'class':'form-control'}),
        
#         }
# Person_CHOICES =(
#     # ("Faculty Member", "Faculty Member"),
#     ("Staff", "Staff"),
#     ("Student", "Student"),
# )

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        
        # depts = forms.ModelMultipleChoiceField(
        #                widget = forms.SelectMultiple(attrs={'class':'form-control'}),
        #                queryset = Dept.objects.all()
        #        )
        # ,'user_type'
        fields = ['first_name','last_name','email_id','contact_no','gender','designation','depts']
        exclude = ['user_type','meetings','staff_id']
        # labels = {
        #     'first_name': ('First Name'),
        #     'last_name': ('Last Name'),
        #     'email_id': ('Email'),
        #     'contact_no':('Contact Number'),
        #     'gender':('Gender'),
        #     'designation': ('Designation'),
        #     'depts':('Department'),
        #     # 'user_type':('User Type')
        # }
        
        # widgets = {
        # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
        # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
        # 'email_id':forms.EmailInput(attrs={'class':'form-control'}),
        # 'contact_no':forms.TextInput(attrs={'class':'form-control'}),
        # 'gender':forms.Select(attrs={'class':'form-control'}),
        # 'designation':forms.Select(attrs={'class':'form-control'}),
        # 'depts':forms.Select(attrs={'class':'form-control'}),
        # 'user_type':forms.Select(attrs={'class':'form-control'}),
        # }        

class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        
        fields = ['designation_name','comments'] 
        
        labels = {
            'designation_name': ('Designation Name'),
            'comments': ('Comments'),
                       
        }
        
        widgets = {
        'designation_name':forms.TextInput(attrs={'class':'form-control '}),
        'comments':forms.TextInput(attrs={'class':'form-control '}),
        
         }
       
class FacultyMemberForm(forms.ModelForm):
    class Meta:
        model = FacultyMember
        # fields ='__all__'
        # depts = forms.ModelMultipleChoiceField(
        # queryset=Dept.objects.all(),
        # widget=forms.CheckboxSelectMultiple
        # )
        # depts = forms.ModelMultipleChoiceField(
        #                widget = forms.SelectMultiple(attrs={'class':'form-control'}),
        #                queryset = Dept.objects.all()
            #    )
        # depts = models.ManyToManyField(Dept)
        fields = ['first_name','last_name','email_id','contact_no','gender','designation','depts','user_type']
        exclude = ['meetings','facultymember_id']
        # labels = {
        #     'first_name': ('First Name'),
        #     'last_name': ('Last Name'),
        #     'email_id': ('Email'),
        #     'contact_no':('Contact Number'),
        #     'gender':('Gender'),
        #     'designation': ('Designation'),
        #     'depts':('Departments'),
        #     'user_type':('User Type'),
        # }
        
        # widgets = {
        # 'first_name':forms.TextInput(attrs={'class':'form-control'}),
        # 'last_name':forms.TextInput(attrs={'class':'form-control'}),
        # 'email_id':forms.EmailInput(attrs={'class':'form-control'}),
        # # 'contact_no':forms.(attrs={'class':'form-control'}),
        # 'gender':forms.Select(attrs={'class':'form-control'}),
        # 'designation':forms.Select(attrs={'class':'form-control'}),
        # 'contact_no':forms.TextInput(attrs={'class':'form-control'}),
        # 'depts':forms.Select(attrs={'class':'form-control'}),
        # 'user_type':forms.TextInput(attrs={'class':'form-control','disabled':True}),
        # ,'hidden':True
        # 'depts':forms.ModelMultipleChoiceField(attrs={'class':'form-control'}),queryset = Dept.objects.all(),
        # }        



class ComplainForm(forms.ModelForm):
    # searching = forms.TextInput(attrs={'class':'form-control'})
    # widget=forms.TextInput(attrs={'class': 'form-control','name' : 'q'})
    # searching = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','name' : 'q', 'type':'search'}))
    # offenders = forms.ModelMultipleChoiceField(
    # queryset=Student.objects.all(), 
    # queryset=Student.objects.exclude(student_id=complainant),
    # attrs={'class':'form-control'},
    # queryset=Student.objects.all(),
    # required=False,
    # widget=FilteredSelectMultiple(attrs={'class':'form-control'},
    # verbose_name=('Student'),
    #   is_stacked=False
    # )
#   )
    class Meta:
        
        model = Complain
        
        # fields = ['complain_date','faculty_complainant','staff_complainant','student_complainant','offenders','offences','complain_detail']
        fields = ['complain_date','incident_date','complainant','offenders','offences','complain_detail']
        exclude =['meetings','meeting_assigned','attendance_done','complain_completed']
        
        # autocomplete_fields = ["offenders"]
        # offenders = forms.ModelMultipleChoiceField(
        # widget = forms.CheckboxSelectMultiple,
        
        # if (searching)
        # queryset = Student.objects.filter(student_id=searching)
        #         )
        # else queryset = Student.objects.all(),
        
        # offences = forms.ModelMultipleChoiceField(
        #             #    widget = forms.CheckboxSelectMultiple,
        #                queryset = Offence.objects.all()
        #        )
        
        offenders = forms.ModelMultipleChoiceField(
                       widget = forms.SelectMultiple(attrs={'class':'form-control'}),
                       queryset = Student.objects.all()
               )
        
        offences = forms.ModelMultipleChoiceField(
                       widget = forms.SelectMultiple(attrs={'class':'form-control'}),
                       queryset = Offence.objects.all()
               )
                
        labels = {
            'complain_date': ('Complain Date'),
            'incident_date': ('Incident Date'),
            'complainant': ('Complainant'),
            'offenders': ('Offenders'),
            'offences': ('Offences'),
            'complain_detail': ('Complain Detail'),
            
            
        }
        widgets = {
        'complain_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control datetimepicker-input', 'placeholder':'Select a date', 'type':'date'}),
        'incident_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control datetimepicker-input', 'placeholder':'Select a date', 'type':'date'}),
        # 'offenders':forms.SelectMultiple(attrs={'class':'form-control'}),
        'complainant':forms.Select(attrs={'class':'form-control '}),
        'offenders':forms.SelectMultiple(attrs={'class':'form-control'}),
        'offences':forms.SelectMultiple(attrs={'class':'form-control'}),
        # 'register_by':forms.Select(attrs={'class':'form-control'}),
        'complain_detail':forms.Textarea(attrs={'class':'form-control placeholder="Provide Detail','rows':3}),
        }
        
class OffenceForm(forms.ModelForm):
    class Meta:
        model = Offence
        fields = ['offence_name','comments']
        
        labels = {
            'offence_name': ('Offence Name'),
            'comments': ('Offence comments'),
            
        }
        
        widgets = {
        'offence_name':forms.TextInput(attrs={'class':'form-control'}),
        'comments':forms.TextInput(attrs={'class':'form-control'}),
        }
        
class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['penalty_name','comments']
        exclude = ['decisions']
        labels = {
            'penalty_name': ('Penalty Name'),
            'comments': ('Penalty Comments'),
            
        }
        widgets = {
        'penalty_name':forms.TextInput(attrs={'class':'form-control'}),
        'comments':forms.TextInput(attrs={'class':'form-control'}),
        }
        
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        # meeting_date = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': today, 'type': 'date'}), required=True)
        # fields ='__all__'
        fields = ['meeting_date','meeting_location','chair_by','complains','comments']
        # 'register_by':forms.Select(attrs={'class':'form-control'}),
        exclude = ['attendees','comments']
        labels = {
            'complains': ('Complains'),
        }
        widgets = {
        'meeting_location':forms.Select(attrs={'class':'form-control '}),
        'chair_by':forms.Select(attrs={'class':'form-control '}),
        # 'complains': forms.CheckboxSelectMultiple(attrs={'class':'form-control checkbox checkbox-primary'}),
        'complains':forms.SelectMultiple(attrs={'class':'form-control'}),
        'meeting_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control datetimepicker-input', 'placeholder':'Select a date', 'type':'date'}),
        'comments':forms.TextInput(attrs={'class':'form-control'}),              
        }
        # forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        # widgets = {
        #     'complains': forms.CheckboxSelectMultiple(),
        # }
        # fields = ['first_name','last_name']
        # meeting_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
        # fields = ['meeting_date','meeting_location','chair_by','attendees','comments']
        
        # widgets = {
        #     'meeting_date': DatePicker(),
        # }
        
# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         fields = ['id','meeting','complain','attendee','attendance_status','comments']
#         # fields ='__all__' 
#         widgets = {
#         'id':forms.TextInput(attrs={'class':'form-control'}),
#         'meeting':forms.Select(attrs={'class':'form-control '}),
#         'complain':forms.Select(attrs={'class':'form-control '}),
#         'attendee':forms.Select(attrs={'class':'form-control '}),
#         'attendance_status':forms.Select(attrs={'class':'form-control'}),
#         'comments':forms.TextInput(attrs={'class':'form-control'}),
#         # 'complains': forms.CheckboxSelectMultiple(attrs={'class':'form-control checkbox checkbox-primary'}),
#         # 'attendee':forms.CheckboxSelectMultiple(),
#         # 'meeting_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
#         }

class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ['id','complain','offender_student','meeting','penalties','comments']
        # fields ='__all__'
        widgets = {
        'id':forms.TextInput(attrs={'class':'form-control'}),
        'offender_student':forms.Select(attrs={'class':'form-control'}),
        'penalties':forms.Select(attrs={'class':'form-control'}),
        'complain':forms.Select(attrs={'class':'form-control'}),
        # 'complain':forms.Select(attrs={'class':'form-control '}),
        'meeting':forms.Select(attrs={'class':'form-control'}),
        'comments':forms.TextInput(attrs={'class':'form-control'}),
        
        
        # 'complains': forms.CheckboxSelectMultiple(attrs={'class':'form-control checkbox checkbox-primary'}),
        # 'attendee':forms.CheckboxSelectMultiple(),
        # 'meeting_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        } 
        
class StudentDetailForm(forms.ModelForm):
    student_id = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Student ID"
    }))
    
    first_name= forms.CharField(widget=forms.TextInput(attrs={
        # 'type': "number",
        "class": "form-control",
        "placeholder": "First Name"
    }))
    
    last_name= forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last Name"
    }))
        
    contact_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "level"
    }))
    
    gender = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Gender"
    }))
    
    program = forms.CharField(widget=forms.Select(attrs={
        "class": "form-control",
        "placeholder": "Program"
    }))
    
    # widgets = {
    #     'program':forms.Select(attrs={'class':'form-control '}),
        
    #     }
    
    class Meta:
        model = Student
        fields = ['student_id', 'first_name','last_name','contact_no','gender','program'
        ]       


# class EditStudentForm(forms.Form):
#     user_type = forms.ChoiceField(label="User Type", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
#     email_id = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    
#     gender_list = (
#         ('Male','Male'),
#         ('Female','Female')
#     )
#     gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    
#     # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
#     # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
#     profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"})) 


class FYPForm(forms.ModelForm):
    class Meta:
        model = FYP
        fields = ['program', 'title', 'abstract', 'image', 'students', 'supervisor']
        widgets = {
            'students': forms.SelectMultiple(),
        }