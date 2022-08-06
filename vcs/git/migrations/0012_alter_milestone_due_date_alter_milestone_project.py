# Generated by Django 4.0.2 on 2022-07-31 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0011_alter_milestone_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.project'),
        ),
    ]