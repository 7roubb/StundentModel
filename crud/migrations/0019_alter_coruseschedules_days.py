# Generated by Django 4.2.11 on 2024-05-02 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0018_alter_coruseschedules_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coruseschedules',
            name='days',
            field=models.CharField(choices=[('m-w', 'Monday - Wensday'), ('s-t-t', 'Sunday-Tuesday-Thursday')], default='m-w', max_length=10),
        ),
    ]