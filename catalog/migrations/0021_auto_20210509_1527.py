# Generated by Django 3.1.7 on 2021-05-09 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_auto_20210509_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typescard',
            old_name='paysystem',
            new_name='paysystemType',
        ),
    ]
