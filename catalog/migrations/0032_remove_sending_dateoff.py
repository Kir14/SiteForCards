# Generated by Django 3.1.7 on 2021-05-13 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_sending_dateoff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sending',
            name='dateOFF',
        ),
    ]