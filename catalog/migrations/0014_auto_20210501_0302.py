# Generated by Django 3.1.7 on 2021-05-01 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20210501_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='ostatok',
            field=models.CharField(default=0, help_text='Остаток', max_length=100),
        ),
    ]
