# Generated by Django 4.0.2 on 2022-07-16 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('git', '0004_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_open', models.BooleanField(default=True)),
                ('assignees', models.ManyToManyField(blank=True, related_name='assignees', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(blank=True, to='git.Label')),
                ('milestone', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='git.milestone')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.project')),
            ],
        ),
    ]
