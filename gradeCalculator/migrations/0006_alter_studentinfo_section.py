# Generated by Django 5.0.6 on 2024-05-31 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradeCalculator', '0005_alter_studentinfo_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='section',
            field=models.CharField(choices=[('BSIT 2-A Algorithm', 'BSIT 2-A Algorithm'), ('BSIT 2-B Pseudocode', 'BSIT 2-B Pseudocode')], max_length=25),
        ),
    ]
