import datetime
from enum import unique
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_choices=(
    ('Faculty','Faculty'),
    ('Staff','Staff'),
    ('Student','Student'),
    )
    user_type =  models.CharField(max_length=255,choices=user_type_choices)
    
    def __str__(self):
        return self.first_name + " " + self.last_name + " is a " + self.user_type
    
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,blank=True)
    email_id = models.EmailField(max_length=50)
    USER_TYPE_CHOICES=(
    ('facultyMember','Faculty Member'),
    ('Staff','Staff'),
    ('Student','Student'))
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES,blank=True)
    contact_no = models.CharField(max_length=50)
    GENDER_CHOICES=(
    ('MALE','MALE'),
    ('FEMALE','FEMALE'))
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    
     
    objects = models.Manager()
    def __str__(self):
       return self.first_name + " " + self.last_name

class Student(Person):
     
    student_id = models.CharField(max_length=14 ,unique=True)
    complains_against = models.ManyToManyField('Complain', through='Complain_Student')
    program = models.ForeignKey("Program", on_delete=models.PROTECT)
    term = models.ForeignKey("Term", on_delete=models.PROTECT)
    
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
       
    objects = models.Manager()
    def __str__(self):
        return self.student_id 
    
class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)
    comments = models.CharField(max_length=255,blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.faculty_name

class Faculty_Audit(models.Model):
    username = models.CharField(max_length=30)
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

class Designation(models.Model):
    designation_name = models.CharField(max_length=55)
    comments = models.TextField(max_length=255,blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Department object (in Admin site etc.)."""
        return self.designation_name
    
class Dept(models.Model):
    dept_name = models.CharField(max_length=255,unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    locations=(
    ('Block A','Block A'),
    ('Block B','Block B'),
    ('Block C','Block C'),
    ('Block D','Block D')
    )
    dept_location = models.CharField(max_length=255,choices=locations)
    faculty_members = models.ManyToManyField('FacultyMember', through='Dept_FacultyMember')
    staff_members  = models.ManyToManyField('Staff', through='Dept_Staff')
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Department object (in Admin site etc.)."""
        return self.dept_name

class Term(models.Model):
    term_name = models.CharField(max_length=5)
    term_start_date = models.DateField()
    term_end_date = models.DateField()
    comments = models.CharField(max_length=255,blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    def __str__(self):
       return self.term_name

class Program(models.Model):
    program_name = models.CharField(max_length=255,unique=True)
    program_code = models.CharField(max_length=4,unique=True)
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    PROGRAM_TYPE_CHOICES=(
    ('UNDERGRADUATE','UNDERGRADUATE'),
    ('GRADUATE','GRADUATE'),
    ('DOCTRATE','DOCTRATE'),
    )
    program_type = models.CharField(max_length=255,choices=PROGRAM_TYPE_CHOICES)
    comments = models.TextField(max_length=255,blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Program object (in Admin site etc.)."""
        return self.program_code
    class Meta:
       unique_together = [['program_name','dept']]
    
class Staff(Person):
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT)
    depts = models.ManyToManyField('Dept', through='Dept_Staff')
    committees = models.ManyToManyField('Committee', through='Staff_Committee',blank=True)
    comments = models.TextField(max_length=255,blank=True)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
       """String for representing the Faculty object (in Admin site etc.)."""
       return self.first_name + " " + self.last_name
   
class Dept_Staff(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    # dept_join_date = models.DateField()
    # dept_end_date = models.DateField()
    def __str__(self):
        """String for representing the Faculty object (in Admin site etc.)."""
        return self.staff + " is inz " + self.dept

class FacultyMember(Person):
    facultymember_id = models.CharField(max_length=255,blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT)
    depts = models.ManyToManyField('Dept', through='Dept_FacultyMember')
    committees = models.ManyToManyField('Committee', through='FacultyMember_Committee',blank=True)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Dept_FacultyMember(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.PROTECT)
    faculty_member = models.ForeignKey(FacultyMember, on_delete=models.PROTECT)
    # dept_join_date = models.DateField()
    # dept_end_date = models.DateField()
    def __str__(self):
        """String for representing the Faculty object (in Admin site etc.)."""
        return str(self.faculty_member)
       


class Committee(models.Model):
    committee_name = models.CharField(max_length=255)
    faculty_members = models.ManyToManyField("FacultyMember", through='FacultyMember_Committee')
    staff_members = models.ManyToManyField("Staff", through='Staff_Committee')
    headed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='headed_by_set')
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
            
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return str(self.committee_id)

class FacultyMember_Committee(models.Model):
    faculty_member = models.ForeignKey(FacultyMember, on_delete=models.PROTECT)
    committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
   
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.faculty_member + " " + self.commitee

class Staff_Committee(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
   
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.staff + " " + self.commitee

    
# class Dept_FacultyMember(models.Model):
#     dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
#     faculty_member = models.ForeignKey(FacultyMember, on_delete=models.CASCADE)
#     desig = models.CharField(max_length=255)
#     dept_join_date = models.DateField()
#     dept_end_date = models.DateField()
    
#     objects = models.Manager()
#     def __str__(self):
#         """String for representing the Meeting object (in Admin site etc.)."""
#         return self.faculty_member + " is in " + self.dept


   
class Meeting(models.Model):
    meeting_date = models.DateField()
    locations=(
    ('President Conference Room','President Conference Room'),
    ('Block D Conference Room','Block D Conference Room'),
    ('Block B Conference Room','Block B Conference Room'),
    )
    meeting_location = models.CharField(max_length=255,choices=locations,blank=True)
    chair_by = models.ForeignKey("Person", on_delete=models.PROTECT,related_name='chair_by_set',blank=True,null=True)
    complains = models.ManyToManyField("Complain", through='Complain_Meeting')
    # decisions = models.ManyToManyField("Decision", through='Meeting_Decision',blank=True)
    comments = models.TextField(max_length=255)
    record_created_at = models.DateTimeField(auto_now_add=True)
    record_updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        # return "Meeting held at " + str(self.meeting_location) + " on " + str(self.meeting_date)
        return "Meeting held" + " on " + str(self.meeting_date)

   
class FacultyMember_Meeting(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    faculty_member = models.ForeignKey(FacultyMember, on_delete=models.PROTECT)
    
    objects = models.Manager()
    def __str__(self):
        return self.faculty_member + " attends " + self.faculty_meeting


    
    # class Meta:
    #     abstract = True
    
    objects = models.Manager()
    def __str__(self):
        return self.studentid 


  
class Complainant(Student):
    comments = models.TextField(max_length=255)
    record_changed_at = models.DateTimeField(auto_now_add=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.studentid 
    
class Offender(Student):
    # complains_against = models.ManyToManyField('Complain', through='Decision')
    comments = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.studentid 

class Complain(models.Model):
    complain_date = models.DateField()
    incident_date = models.DateField()
    # student_complainant = models.ForeignKey("Student", on_delete=models.CASCADE,related_name='student_complainant_set',blank=True,null=True)
    # faculty_complainant = models.ForeignKey("FacultyMember", on_delete=models.CASCADE,related_name='faculty_complainant_set',blank=True,null=True)
    # staff_complainant = models.ForeignKey("Staff", on_delete=models.CASCADE,related_name='staff_complainant_set',blank=True,null=True)
    complainant = models.ForeignKey("Person", on_delete=models.PROTECT,related_name='complainant_set',blank=True,null=True)
    
    offenders = models.ManyToManyField("Student", through='Complain_Student',verbose_name="Student",related_name='students_set')
    offences = models.ManyToManyField("Offence", through='Complain_Offence')
    # register_by = models.ForeignKey('Person', on_delete=models.CASCADE)
    complain_detail = models.TextField(max_length=50)
    meetings = models.ManyToManyField("Meeting", through='Complain_Meeting',blank=True )
    meeting_assigned = models.BooleanField(default=False,blank=True)
    attendance_done = models.BooleanField(default=False,blank=True)
    complain_completed = models.BooleanField(default=False,blank=True)
    # comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        return "Complain_" + str(self.id)

class Complain_FacultyMember(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    Staff = models.ForeignKey(FacultyMember, on_delete=models.PROTECT)

class Complain_Staff(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    Staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    
    objects = models.Manager()
    def __str__(self):
        return self.complain + " " + self.student
    
class Complain_Student(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    Student = models.ForeignKey(Student, on_delete=models.PROTECT)
    
    objects = models.Manager()
    def __str__(self):
        return self.complain + " " + self.student

class Penalty(models.Model):
    penalty_name = models.CharField(max_length=255,unique=True)
    comments = models.CharField(max_length=255)
    decisions = models.ManyToManyField('Decision', through='Decision_Penalty',blank=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
       
    objects = models.Manager()
    def __str__(self):
        """String for representing the Penalty object (in Admin site etc.)."""
        return self.penalty_name

class Decision(models.Model):
    offender_student = models.ForeignKey(Student, on_delete=models.PROTECT)
    penalties = models.ManyToManyField("Penalty", through='Decision_Penalty')
    # meetings = models.ManyToManyField("Meeting", through='Meeting_Decision',blank=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT,blank=True)
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT,blank=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Penalty object (in Admin site etc.)."""
        return self.comments

class Decision_Penalty(models.Model):
    id = models.AutoField(primary_key=True)
    decision = models.ForeignKey(Decision, on_delete=models.PROTECT)
    penalty = models.ForeignKey(Penalty, on_delete=models.PROTECT,blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.decision
    
# class Meeting_Decision(models.Model):
#     meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
#     decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    
#     objects = models.Manager()
#     def __str__(self):
#         """String for representing the Meeting object (in Admin site etc.)."""
#         return self.meeting + " have " + self.decision
    
class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT)
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    # complainant_attendee = models.ForeignKey(Student, on_delete=models.CASCADE)
    # offender_attendee = models.ForeignKey(Student, on_delete=models.CASCADE)
    # faculty_attendee = models.ForeignKey(FacultyMember, on_delete=models.CASCADE)
    # staff_attendee = models.ForeignKey(Staff, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Person, on_delete=models.PROTECT)
    
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
       return self.attendee + " " + self.attendance_status

class Offence(models.Model):
    offence_name = models.CharField(max_length=255)
    complains = models.ManyToManyField("Complain", through='Complain_Offence',blank=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        return self.offence_name

class Complain_Offence(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    offence = models.ForeignKey(Offence, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.id
    
class Complain_Meeting(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    meeting = models.ForeignKey(Meeting, on_delete=models.PROTECT,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.comments
      
class Complain_Committee(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.PROTECT)
    committee = models.ForeignKey(Committee, on_delete=models.PROTECT)
    
    objects = models.Manager()
    def __str__(self):
        """String for representing the Meeting object (in Admin site etc.)."""
        return self.complain + " " + self.commitee
    
class FYP(models.Model):
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='fyps')
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    image = models.ImageField(upload_to='fyp_images')
    students = models.ManyToManyField('Student', related_name='fyp_students')
    supervisor = models.ForeignKey('FacultyMember', on_delete=models.PROTECT, related_name='supervised_fyps')
    
    def __str__(self):
        return self.title