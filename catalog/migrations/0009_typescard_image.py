# Generated by Django 3.1.7 on 2021-04-20 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_card_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='typescard',
            name='image',
            field=models.ImageField(blank=True, default='Batman.jpg', null=True, upload_to=''),
        ),
    ]
