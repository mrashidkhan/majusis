from django.urls import path, include
from sdasapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('dual_listbox/', views.dual_listbox, name="dual_listbox"),
    # path('change_password/', views.change_password, name="change_password"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('user_signin/', views.user_signin, name="user_signin"),
    path('user_signout/', views.user_signout, name="user_signout"),
    
    path('register_complain/', views.register_complain, name="register_complain"),
    
    path('add_faculty/', views.add_faculty, name="add_faculty"),
    path('faculty_read/', views.faculty_read, name="faculty_read"),
    path('faculty_delete/<int:id>/', views.faculty_delete, name="faculty_delete"),
    path('faculty_edit/<int:id>/', views.faculty_edit, name="faculty_edit"),
    path('faculty_update/<int:id>/', views.faculty_update, name="faculty_update"),
    path('faculty_detail/<int:id>/', views.faculty_detail, name="faculty_detail"),
    
    path('add_designation/', views.add_designation, name="add_designation"),
    path('designation_read/', views.designation_read, name="designation_read"),
    path('designation_edit/<int:id>/', views.designation_edit, name="designation_edit"),
    path('designation_update/<int:id>/', views.designation_update, name="designation_update"),
    path('designation_delete/<int:id>/', views.designation_delete, name="designation_delete"),
    path('designation_detail/<int:id>/', views.designation_detail, name="designation_detail"),
    
    path('add_dept/', views.add_dept, name="add_dept"),
    path('dept_read/', views.dept_read, name="dept_read"),
    path('dept_edit/<int:id>/', views.dept_edit, name="dept_edit"),
    path('dept_update/<int:id>/', views.dept_update, name="dept_update"),
    path('dept_detail/<int:id>/', views.dept_detail, name="dept_detail"),
    
    path('add_term/', views.add_term, name="add_term"),
    path('term_read/', views.term_read, name="term_read"),
    path('term_edit/<int:id>/', views.term_edit, name="term_edit"),
    path('term_update/<int:id>/', views.term_update, name="term_update"),
    path('term_delete/<int:id>/', views.term_delete, name="term_delete"),
    path('term_detail/<int:id>/', views.term_detail, name="term_detail"),
    
    path('add_program/', views.add_program, name="add_program"),
    path('program_read/', views.program_read, name="program_read"),
    path('program_edit/<int:id>/', views.program_edit, name="program_edit"),
    path('program_update/<int:id>/', views.program_update, name="program_update"),
    path('program_detail/<int:id>/', views.program_detail, name="program_detail"),
    
    # path('add_acad_depart/', views.add_acad_depart, name="add_acad_depart"),
    # path('add_program_type/', views.add_program_type, name="add_program_type"),
        
    path('add_staff/', views.add_staff, name="add_staff"),
    path('staff_read/', views.staff_read, name="staff_read"),
    path('staff_edit/<int:id>/', views.staff_edit, name="staff_edit"),
    path('staff_update/<int:id>/', views.staff_update, name="staff_update"),
    path('staff_delete/<int:id>/', views.staff_delete, name="staff_delete"),
    path('staff_detail/<int:id>/', views.staff_detail, name="staff_detail"),
    
    path('add_student/', views.add_student, name="add_student"),
    path('student_read/', views.student_read, name="student_read"),
    path('student_edit/<int:id>/', views.student_edit, name="student_edit"),
    path('student_update/<int:id>/', views.student_update, name="student_update"),
    path('student_detail/<int:id>', views.student_detail, name="student_detail"),
   
    path('add_facultymember/', views.add_facultymember, name="add_facultymember"),
    path('facultymember/', views.facultymember_read, name="facultymember_read"),
    path('facultymember_edit/<int:id>/', views.facultymember_edit, name="facultymember_edit"),
    path('facultymember_update/<int:id>/', views.facultymember_update, name="facultymember_update"),
    path('facultymember_delete/<int:id>/', views.facultymember_delete, name="facultymember_delete"),
    path('facultymember_detail/<int:id>/', views.facultymember_detail, name="facultymember_detail"),
    
    
    path('add_offence/', views.add_offence, name="add_offence"),
    path('offence_read/', views.offence_read, name="offence_read"),
    
    path('add_complain/', views.add_complain, name="add_complain"),
    path('complain_read/', views.complain_read, name="complain_read"),
    
    
    path('search_student/', views.search_student, name="search_student"),
    
        
    path('add_meeting/', views.add_meeting, name="add_meeting"),
    path('meeting_read/', views.meeting_read, name="meeting_read"),
    
    path('add_attendance/', views.add_attendance, name="add_attendance"),
    path('attendance_read/', views.attendance_read, name="attendance_read"),
    
    path('add_penalty/', views.add_penalty, name="add_penalty"),
    path('penalty_read/', views.penalty_read, name="penalty_read"),
    
    path('add_decision/', views.add_decision, name="add_decision"),
    path('decision_read/', views.decision_read, name="decision_read"),
    path('multi_select/', views.multi_select, name="multi_select"),
    
    # path('student_detail/<int:id>/', views.student_detail, name="student_detail"),
    path('student_delete/<int:id>/', views.student_delete, name="student_delete"),
    
    # path('faculty_detail/<int:id>/', views.faculty_detail, name="faculty_detail"),
    
    
    
    
    # path('dept_detail/<int:id>/', views.dept_detail, name="student_detail"),
    path('dept_delete/<int:id>/', views.dept_delete, name="dept_delete"),
    
    # path('program_detail/<int:id>/', views.program_detail, name="program_detail"),
    path('program_delete/<int:id>/', views.program_delete, name="program_delete"),
    
    path('offence_detail/<int:id>/', views.offence_detail, name="offence_detail"),
    path('offence_delete/<int:id>/', views.offence_delete, name="offence_delete"),
    path('offence_edit/<int:id>/', views.offence_edit, name="offence_edit"),
    path('offence_update/<int:id>/', views.offence_update, name="offence_update"),
    
    path('complain_detail/<int:id>/', views.complain_detail, name="complain_detail"),
    path('complain_edit/<int:id>/', views.complain_edit, name="complain_edit"),
    path('complain_update/<int:id>/', views.complain_update, name="complain_update"),
    path('complain_delete/<int:id>/', views.complain_delete, name="complain_delete"),
    
    path('meeting_detail/<int:id>/', views.meeting_detail, name="meeting_detail"),
    path('meeting_edit/<int:id>/', views.meeting_edit, name="meeting_edit"),
    path('meeting_update/<int:id>/', views.meeting_update, name="meeting_update"),
    path('meeting_delete/<int:id>/', views.meeting_delete, name="meeting_delete"),
    
    # path('attendance_detail/<int:id>/', views.attendance_detail, name="attendance_detail"),
    path('attendance_delete/<int:id>/', views.attendance_delete, name="attendance_delete"),
    
    path('penalty_edit/<int:id>/', views.penalty_edit, name="penalty_edit"),
    path('penalty_update/<int:id>/', views.penalty_update, name="penalty_update"),
    path('penalty_detail/<int:id>/', views.penalty_detail, name="penalty_detail"),
    path('penalty_delete/<int:id>/', views.penalty_delete, name="penalty_delete"),
    
    
    # path('decision_detail/<int:id>/', views.decision_detail, name="decision_detail"),
    path('decision_delete/<int:id>/', views.decision_delete, name="decision_delete"),
    
    path('ajax_load_complainants/', views.load_complainants, name="ajax_load_complainants"),
    path('ajax_complain_offenders/', views.ajax_complain_offenders, name="ajax_complain_offenders"),
    path('ajax_load_students/', views.load_students, name="ajax_load_students"),
    
    
    # For Add Attendance Form
    path('ajax_attendance_meeting/', views.ajax_attendance_meeting, name="ajax_attendance_meeting"),
    path('ajax_attendance_complainant/', views.ajax_attendance_complainant, name="ajax_attendance_complainant"),
    path('ajax_attendance_offenders/', views.ajax_attendance_offenders, name="ajax_attendance_offenders"),
    
    # For Add Decision Form
    path('ajax_decision_meeting/', views.ajax_decision_meeting, name="ajax_decision_meeting"),
    path('ajax_decision_complain/', views.ajax_decision_complain, name="ajax_decision_complain"),
    # path('ajax_decision_offenders/', views.ajax_decision_offenders, name="ajax_decision_offenders"),
    
       
    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change_password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    # For Report Designing
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('complain_report/', views.complain_report, name='complain_report'),
    # path('complain/<int:pk>/', ComplainDetailView.as_view(), name='complain_detail')
]    
    