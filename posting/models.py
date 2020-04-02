from django.db import models
from django.contrib.auth.models import User

CLASS_CHOICES = [
    ('All', 'All'),
    ('Cos126', 'Cos126'),
    ('Cos217', 'Cos217'),
    ('Cos226', 'Cos226'),
    ('Cos333', 'Cos333'),
    ('Cos340', 'Cos340'),
]

# Create your models here.
class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.TextField(default='', blank=True)
    title = models.TextField()
    link = models.TextField()
    embed_link = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    num_views = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    description = models.TextField()
    class_choice = models.CharField(max_length=30, blank=False, choices=CLASS_CHOICES) 

class Comments(models.Model):
    video      = models.ForeignKey(Video, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
