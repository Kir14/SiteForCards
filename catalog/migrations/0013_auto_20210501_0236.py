# Generated by Django 3.1.7 on 2021-04-30 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_sending_checkbox'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='password',
            field=models.CharField(default='1234', help_text='Пароль', max_length=100),
        ),
    ]