# Generated by Django 4.1.2 on 2023-01-02 15:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sdasapp', '0003_alter_complain_complainant'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='incident_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]