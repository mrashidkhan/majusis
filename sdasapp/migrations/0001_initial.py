# Generated by Django 4.1.2 on 2022-12-25 15:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('Faculty', 'Faculty'), ('Staff', 'Staff'), ('Student', 'Student')], max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee_name', models.CharField(max_length=255)),
                ('comments', models.TextField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
                ('headed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='headed_by_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain_date', models.DateField()),
                ('complain_detail', models.TextField(max_length=50)),
                ('meeting_assigned', models.BooleanField(default=False)),
                ('complain_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Complain_Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
            ],
        ),
        migrations.CreateModel(
            name='Complain_Offence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
            ],
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complain', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
            ],
        ),
        migrations.CreateModel(
            name='Decision_Penalty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('decision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.decision')),
            ],
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=255, unique=True)),
                ('dept_location', models.CharField(choices=[('Block A', 'Block A'), ('Block B', 'Block B'), ('Block C', 'Block C'), ('Block D', 'Block D')], max_length=255)),
                ('comments', models.TextField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation_name', models.CharField(max_length=55)),
                ('comments', models.TextField(blank=True, max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_name', models.CharField(max_length=255)),
                ('comments', models.CharField(blank=True, max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty_Audit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('action', models.CharField(choices=[('Created', 'Created'), ('Updated', 'Updated'), ('Deleted', 'Deleted')], max_length=255)),
                ('changes', models.CharField(max_length=255)),
                ('action_date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_date', models.DateField()),
                ('meeting_location', models.CharField(blank=True, choices=[('President Conference Room', 'President Conference Room'), ('Block D Conference Room', 'Block D Conference Room'), ('Block B Conference Room', 'Block B Conference Room')], max_length=255)),
                ('comments', models.TextField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
                ('complains', models.ManyToManyField(through='sdasapp.Complain_Meeting', to='sdasapp.complain')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('email_id', models.EmailField(max_length=50)),
                ('user_type', models.CharField(choices=[('facultyMember', 'facultyMember'), ('Staff', 'Staff'), ('Student', 'Student')], max_length=20)),
                ('contact_no', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_name', models.CharField(max_length=5)),
                ('term_start_date', models.DateField(blank=True)),
                ('term_end_date', models.DateField(blank=True)),
                ('comments', models.CharField(blank=True, max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FacultyMember',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sdasapp.person')),
                ('facultymember_id', models.CharField(blank=True, max_length=255)),
                ('comments', models.TextField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('sdasapp.person',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sdasapp.person')),
                ('comments', models.TextField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('sdasapp.person',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sdasapp.person')),
                ('student_id', models.CharField(max_length=14, unique=True)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('sdasapp.person',),
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=255, unique=True)),
                ('program_code', models.CharField(max_length=4, unique=True)),
                ('program_type', models.CharField(choices=[('UNDERGRADUATE', 'UNDERGRADUATE'), ('GRADUATE', 'GRADUATE'), ('DOCTRATE', 'DOCTRATE')], max_length=255)),
                ('comments', models.TextField(blank=True, max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.dept')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.term')),
            ],
            options={
                'unique_together': {('program_name', 'dept')},
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_name', models.CharField(max_length=255, unique=True)),
                ('comments', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('decisions', models.ManyToManyField(blank=True, through='sdasapp.Decision_Penalty', to='sdasapp.decision')),
            ],
        ),
        migrations.CreateModel(
            name='Offence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offence_name', models.CharField(max_length=255)),
                ('comments', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('complains', models.ManyToManyField(blank=True, through='sdasapp.Complain_Offence', to='sdasapp.complain')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting_Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.decision')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.meeting')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='decisions',
            field=models.ManyToManyField(blank=True, through='sdasapp.Meeting_Decision', to='sdasapp.decision'),
        ),
        migrations.CreateModel(
            name='Dept_Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.dept')),
            ],
        ),
        migrations.CreateModel(
            name='Dept_FacultyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.dept')),
            ],
        ),
        migrations.AddField(
            model_name='dept',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.faculty'),
        ),
        migrations.AddField(
            model_name='decision_penalty',
            name='penalty',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='sdasapp.penalty'),
        ),
        migrations.AddField(
            model_name='decision',
            name='meetings',
            field=models.ManyToManyField(blank=True, through='sdasapp.Meeting_Decision', to='sdasapp.meeting'),
        ),
        migrations.AddField(
            model_name='decision',
            name='penalties',
            field=models.ManyToManyField(through='sdasapp.Decision_Penalty', to='sdasapp.penalty'),
        ),
        migrations.CreateModel(
            name='Complain_Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
            ],
        ),
        migrations.AddField(
            model_name='complain_offence',
            name='offence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.offence'),
        ),
        migrations.AddField(
            model_name='complain_meeting',
            name='meeting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sdasapp.meeting'),
        ),
        migrations.CreateModel(
            name='Complain_Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.committee')),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
            ],
        ),
        migrations.AddField(
            model_name='complain',
            name='complainant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complainant_set', to='sdasapp.person'),
        ),
        migrations.AddField(
            model_name='complain',
            name='meetings',
            field=models.ManyToManyField(blank=True, through='sdasapp.Complain_Meeting', to='sdasapp.meeting'),
        ),
        migrations.AddField(
            model_name='complain',
            name='offences',
            field=models.ManyToManyField(through='sdasapp.Complain_Offence', to='sdasapp.offence'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_status', models.CharField(choices=[('ABSENT', 'ABSENT'), ('PRESENT', 'PRESENT')], max_length=200)),
                ('comments', models.CharField(max_length=255)),
                ('record_created_at', models.DateTimeField(auto_now_add=True)),
                ('record_updated_at', models.DateTimeField(auto_now=True)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.person')),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Complainant',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sdasapp.student')),
                ('comments', models.TextField(max_length=255)),
                ('record_changed_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('sdasapp.student',),
        ),
        migrations.CreateModel(
            name='Offender',
            fields=[
                ('student_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sdasapp.student')),
                ('comments', models.TextField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            bases=('sdasapp.student',),
        ),
        migrations.AddField(
            model_name='student',
            name='complains_against',
            field=models.ManyToManyField(through='sdasapp.Complain_Student', to='sdasapp.complain'),
        ),
        migrations.AddField(
            model_name='student',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.program'),
        ),
        migrations.AddField(
            model_name='student',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.term'),
        ),
        migrations.CreateModel(
            name='Staff_Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.committee')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.staff')),
            ],
        ),
        migrations.AddField(
            model_name='staff',
            name='committees',
            field=models.ManyToManyField(blank=True, through='sdasapp.Staff_Committee', to='sdasapp.committee'),
        ),
        migrations.AddField(
            model_name='staff',
            name='depts',
            field=models.ManyToManyField(through='sdasapp.Dept_Staff', to='sdasapp.dept'),
        ),
        migrations.AddField(
            model_name='staff',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.designation'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='chair_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.facultymember'),
        ),
        migrations.CreateModel(
            name='FacultyMember_Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.meeting')),
                ('faculty_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.facultymember')),
            ],
        ),
        migrations.CreateModel(
            name='FacultyMember_Committee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.committee')),
                ('faculty_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.facultymember')),
            ],
        ),
        migrations.AddField(
            model_name='facultymember',
            name='committees',
            field=models.ManyToManyField(blank=True, through='sdasapp.FacultyMember_Committee', to='sdasapp.committee'),
        ),
        migrations.AddField(
            model_name='facultymember',
            name='depts',
            field=models.ManyToManyField(through='sdasapp.Dept_FacultyMember', to='sdasapp.dept'),
        ),
        migrations.AddField(
            model_name='facultymember',
            name='designation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.designation'),
        ),
        migrations.AddField(
            model_name='dept_staff',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.staff'),
        ),
        migrations.AddField(
            model_name='dept_facultymember',
            name='faculty_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.facultymember'),
        ),
        migrations.AddField(
            model_name='dept',
            name='faculty_members',
            field=models.ManyToManyField(through='sdasapp.Dept_FacultyMember', to='sdasapp.facultymember'),
        ),
        migrations.AddField(
            model_name='dept',
            name='staff_members',
            field=models.ManyToManyField(through='sdasapp.Dept_Staff', to='sdasapp.staff'),
        ),
        migrations.AddField(
            model_name='decision',
            name='offender_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.student'),
        ),
        migrations.AddField(
            model_name='complain_student',
            name='Student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.student'),
        ),
        migrations.CreateModel(
            name='Complain_Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
                ('Staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Complain_FacultyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.complain')),
                ('Staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sdasapp.facultymember')),
            ],
        ),
        migrations.AddField(
            model_name='complain',
            name='offenders',
            field=models.ManyToManyField(related_name='students_set', through='sdasapp.Complain_Student', to='sdasapp.student', verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='committee',
            name='faculty_members',
            field=models.ManyToManyField(through='sdasapp.FacultyMember_Committee', to='sdasapp.facultymember'),
        ),
        migrations.AddField(
            model_name='committee',
            name='staff_members',
            field=models.ManyToManyField(through='sdasapp.Staff_Committee', to='sdasapp.staff'),
        ),
    ]
