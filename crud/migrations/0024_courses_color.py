# Generated by Django 4.2.11 on 2024-05-28 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0023_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='color',
            field=models.CharField(default='#FFFFFF', max_length=7),
        ),
    ]