# Generated by Django 4.1.2 on 2023-02-02 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdasapp', '0011_alter_person_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user_type',
            field=models.CharField(blank=True, choices=[('facultyMember', 'Faculty Member'), ('Staff', 'Staff'), ('Student', 'Student')], max_length=20),
        ),
    ]