# Generated by Django 3.0.3 on 2020-04-24 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_auto_20200423_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchfilters',
            name='sort_by',
            field=models.CharField(choices=[('Relevance', 'Relevance'), ('TimeS', 'Shortest Time'), ('Approval', 'Approval (Rating/Likes)'), ('Views', 'Most Views'), ('Comments', 'Most Comments'), ('TimeL', 'Longest Time')], default='Relevance', max_length=3000),
        ),
        migrations.AlterField(
            model_name='youtubedata',
            name='time_length',
            field=models.IntegerField(default=0),
        ),
    ]
