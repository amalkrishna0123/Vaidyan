# Generated by Django 4.1.5 on 2023-07-26 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_alter_appointment_email_alter_appointment_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='accepted_date',
        ),
    ]
