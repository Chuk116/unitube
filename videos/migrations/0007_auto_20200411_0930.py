# Generated by Django 3.0.3 on 2020-04-11 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20200406_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='videos.CommentThread'),
        ),
    ]