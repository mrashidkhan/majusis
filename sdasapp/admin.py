from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.
class UserModel(UserAdmin):
    pass

from sdasapp.models import *

class Faculty_Admin(admin.ModelAdmin):
      list_display = ['id','faculty_name']

admin.site.register(Faculty, Faculty_Admin)

class Dept_Admin(admin.ModelAdmin):
      list_display = ['id','dept_name','dept_location']

admin.site.register(Dept, Dept_Admin)

class Term_Admin(admin.ModelAdmin):
      list_display = ['term_name','term_start_date','term_end_date','comments']

admin.site.register(Term, Term_Admin)


class Program_Admin(admin.ModelAdmin):
      list_display = ['id','program_name','dept','program_type']

admin.site.register(Program, Program_Admin)

class Student_Admin(admin.ModelAdmin):
      list_display = ['student_id','contact_no','gender','program']

admin.site.register(Student, Student_Admin)

class FacultyMember_Admin(admin.ModelAdmin):
      list_display = ['first_name','last_name','email_id','user_type','contact_no','gender']

admin.site.register(FacultyMember, FacultyMember_Admin)

class Staff_Admin(admin.ModelAdmin):
      list_display = ['first_name','last_name','email_id','user_type','contact_no','gender']

admin.site.register(Staff, Staff_Admin)


# class Complain_Admin(admin.ModelAdmin):
#       list_display = ['id','complain_detail','complain_date','complainant','register_by']

# admin.site.register(Complain, Complain_Admin)

# class Meeting_Admin(admin.ModelAdmin):
#       list_display = ['id','meeting_date','meeting_location','chair_by','comments']

# admin.site.register(Meeting, Meeting_Admin)

# class Attendance_Admin(admin.ModelAdmin):
#       list_display = ['id','attendee','attendance_status','comments']

# admin.site.register(Attendance, Attendance_Admin)

class Penalty_Admin(admin.ModelAdmin):
      list_display = ['id','penalty_name','comments']

admin.site.register(Penalty, Penalty_Admin)

# class Decision_Admin(admin.ModelAdmin):
#       list_display = ['id','offender_student','comments']

# admin.site.register(Decision, Decision_Admin)

class Offence_Admin(admin.ModelAdmin):
      list_display = ['id','offence_name']

admin.site.register(Offence, Offence_Admin)
