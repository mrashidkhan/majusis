import datetime
from enum import unique
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    pass
    def __str__(self):
        return self.email
    

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.faculty_name

class Faculty_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    action_date_time = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time


# User Model for Department  
class Dept(models.Model):
    dept_name = models.CharField(max_length=255,unique=True)
    locations=(
    ('Block A','Block A'),
    ('Block B','Block B'),
    ('Block C','Block C'),
    ('Block D','Block D')
    )
    dept_location = models.CharField(max_length=255,choices=locations)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    Staffs  = models.ManyToManyField(Staff, through='Dept_Staff')
    Facultymembers = models.ManyToManyField('FacultyMember', through='Dept_FacultyMember')
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Department object (in Admin site etc.)."""
        return self.dept_name

class Dept_Staff(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.dept + " " + self.staff
    
class Dept_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Staff(Employee):
    desig = models.CharField(max_length=255)
    promotion_date =models.DateField()
    departments = models.ManyToManyField('Dept', through='Dept_Staff')
    meetings = models.ManyToManyField('Meeting', through='Attendance',blank=True)
    committees = models.ManyToManyField('Committee', through='Staff_Committee',blank=True)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.first_name + " " + last_name
   
class Staff_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time


class Program(models.Model):
    program_name = models.CharField(max_length=255,unique=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    PROGRAM_TYPE_CHOICES=(
    ('UNDERGRADUATE','UNDERGRADUATE'),
    ('GRADUATE','GRADUATE'),
    ('DOCTRATE','DOCTRATE'),
    )
    program_type = models.CharField(max_length=255,choices=PROGRAM_TYPE_CHOICES)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Program object (in Admin site etc.)."""
        return self.program_name
    class Meta:
       unique_together = [['program_name','dept']]
       
class Program_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time
       
class Student(models.Model):
    student_id = models.CharField(max_length=30,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    contact_no = models.CharField(max_length=30)
    GENDER_CHOICES=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
    )
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
        return self.student_id 
    
class Student_Audit(models.Model):
    username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time
        
class Offender(Student):
    complains_against = models.ManyToManyField('Complain', through='Decision')
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.student_id 
    
class Offender_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time
    
class Complainant(Student):
    comments = models.TextField(max_length=255)
    record_changed_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    def __str__(self):
        return self.student_id 
    
class Complainant_Audit(models.Model):
    # action_by = request.user
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    contactno = models.CharField(max_length=255)
    GENDER_CHOICES=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE')
    )
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.first_name + " " + self.last_name
   
class FacultyMember(Employee):
    desig = models.CharField(max_length=255)
    desig_start_date =models.DateField()
    desig_end_date =models.DateField()
    departments = models.ManyToManyField('Dept', through='Dept_FacultyMember')
    meetings = models.ManyToManyField('Meeting', through='Attendance',blank=True)
    committees = models.ManyToManyField('Committee', through='FacultyMember_Committee',blank=True)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.first_name + " " + self.last_name
   
class FacultyMember_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Dept_FacultyMember(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    faculty_member = models.ForeignKey(FacultyMember, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.dept + " " + self.faculty_member
    
class Committee(models.Model):
    complains = models.ManyToManyField("Complain", through='Complain_Committee')
    staffs = models.ManyToManyField("Staff", through='Staff_Committee')
    comments = models.TextField(max_length=255)
    headed_by = models.ForeignKey('Employee',blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
            
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return str(self.committee_id)
    
class Complain_Committee(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.complain + " " + self.commitee
    
class Committee_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class FacultyMember_Committee(models.Model):
    faculty_member = models.ForeignKey(FacultyMember, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
   
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.faculty_member + " " + self.commitee

class Staff_Committee(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
   
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.faculty_member + " " + self.commitee


class Meeting(models.Model):
    meeting_date = models.DateField()
    locations=(
    ('President Conference Room','President Conference Room'),
    ('Block D Conference Room','Block D Conference Room'),
    ('Block B Conference Room','Block B Conference Room'),
    )
    meeting_location = models.CharField(max_length=255,choices=locations,blank=True)
    chair_by = models.ForeignKey("Employee", on_delete=models.CASCADE)
    complains = models.ManyToManyField("Complain", through='Complain_Meeting')
    decisions = models.ManyToManyField("Decisions", through='Meeting_Decision',blank=True)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return str(self.meetingid)
    
class Meeting_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255,unique=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Penalty(models.Model):
    penalty_id = models.AutoField(primary_key=True)
    penalty_name = models.CharField(max_length=255,unique=True)
    penalty_comments = models.CharField(max_length=255)
    decisions = models.ManyToManyField('Decision', through='Decision_Penalty',blank=True)
    comments = models.CharField(max_length=255)
    # changed_by = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user.setter
    # def _history_user(self, value):
    #     self.changed_by = value
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Penalty object (in Admin site etc.)."""
        return self.penalty_name
    
class Penalty_Audit(models.Model):
    # action_by = request.user
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255,unique=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Complain(models.Model):
    complain_date = models.DateField()
    complainant = models.ForeignKey(Student, on_delete=models.CASCADE,blank=False, related_name='complainant_set')
    offenders = models.ManyToManyField("Student", through='Complain_Offender',related_name='offenders_set')
    offences = models.ManyToManyField("Offence", through='Complain_Offence')
    register_by = models.ForeignKey('CustomUser')
    complain_detail = models.TextField(max_length=50)
    meetings = models.ManyToManyField("Meeting", through='Complain_Meeting')
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Complain object (in Admin site etc.)."""
        return str(self.complain_id)

class Complain_Offender(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    offender = models.ForeignKey(Offender, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.dept + " " + self.staff

class Complain_Offender(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    offender = models.ForeignKey(Offender, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.dept + " " + self.staff

class Complain_Audit(models.Model):
    # action_by = request.user
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255,unique=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Decision(models.Model):
    decision_id = models.AutoField(primary_key=True)
    offender_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    penalties = models.ManyToManyField(Penalty, through='Decision_Penalty')
    meetings = models.ManyToManyField("Meetings", through='Meeting_Decision',blank=True)
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE,blank=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Penalty object (in Admin site etc.)."""
        return self.decision_comments   

class Decision_Audit(models.Model):
    # action_by = request.user
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255,unique=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time
 
class Meeting_Decision(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    Decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.dept + " " + self.staff
    
class Attendance(models.Model):
    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    ATTENDANCE_CHOICES = (
        ('ABSENT', 'ABSENT'),
        ('PRESENT', 'PRESENT'),
    )
    attendance_status = models.CharField(max_length=200, choices=ATTENDANCE_CHOICES)
    comments = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.attendee + " " + self.attendance_status
   
    class Meta:
       unique_together = [['attendee','meeting']]

class Attendance_Audit(models.Model):
    Username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Offence(models.Model):
    offence_id = models.AutoField(primary_key=True)
    offence_name = models.CharField(max_length=255)
    complains = models.ManyToManyField("Complain", through='Complain_Offence',blank=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Complain object (in Admin site etc.)."""
        return self.offence_name
    
class Offence_Audit(models.Model):
    username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255,unique=True)
    action_date_time = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

   
class Complain_Offence(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    offence = models.ForeignKey(Offence, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.id
    
class Complain_Meeting(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.comments

class Penalty_Audit(models.Model):
    username = models.CharField(max_length=30)
    actions=(
    ('Created','Created'),
    ('Updated','Updated'),
    ('Deleted','Deleted'),
    )
    action = models.CharField(max_length=255,choices=actions)
    changes = models.CharField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.username + " " + self.action + " on " + self.action_date_time

class Decision_Penalty(models.Model):
    id = models.AutoField(primary_key=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    penalty = models.ForeignKey(Penalty, on_delete=models.CASCADE,blank=True)
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.decision
