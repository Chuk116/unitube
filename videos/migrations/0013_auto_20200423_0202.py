# Generated by Django 3.0.3 on 2020-04-23 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0012_auto_20200422_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchfilters',
            name='learning_style',
            field=models.CharField(choices=[('Visual', 'Visual'), ('Verbal', 'Verbal'), ('Aural', 'Aural'), ('Kinesthetic', 'Kinesthetic'), ('Logical', 'Logical')], default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='searchfilters',
            name='sort_by',
            field=models.CharField(choices=[('TimeS', 'Shortest Time'), ('Approval', 'Approval (Rating/Likes)'), ('Views', 'Most Views'), ('Comments', 'Most Comments'), ('TimeL', 'Longest Time')], default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='searchfilters',
            name='sort_using',
            field=models.CharField(choices=[('Unitube', 'Unitube Data'), ('Youtube', 'Youtube Data')], default='Unitube', max_length=3000),
        ),
        migrations.AlterField(
            model_name='searchfilters',
            name='time_length',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('short', 'Short (0 - 5 minutes)'), ('medium', 'Medium (5 - 15 minutes)'), ('semi-long', 'Semi-Long (15 - 25 minutes)'), ('long', 'Long (25+ minutes)')], default='', max_length=27),
        ),
        migrations.AlterField(
            model_name='searchfilters',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
