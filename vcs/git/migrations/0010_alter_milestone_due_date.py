# Generated by Django 4.0.2 on 2022-07-30 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0009_alter_issue_milestone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateTimeField(blank=True),
        ),
    ]
