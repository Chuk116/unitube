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
    uni_video_id = models.TextField(default='', blank=True)
    title = models.TextField()
    link = models.TextField()
    embed_link = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    avg_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    num_ratings = models.IntegerField(default=0)
    num_views = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    description = models.TextField()
    class_choice = models.CharField(max_length=30, blank=False, choices=CLASS_CHOICES)

class YoutubeData(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    title = models.TextField(default='')
    description = models.TextField(default='')
    lang = models.TextField(default='en')
    time_length = models.TextField(default='0')
    num_views = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    tags = models.CharField(max_length=3000, blank=True)

class CommentThread(models.Model):
    video      = models.OneToOneField(Video, on_delete=models.CASCADE)
    num_comments = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    
class Comment(models.Model):
    thread      = models.ForeignKey(CommentThread, on_delete=models.CASCADE, related_name='comments')
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE, related_name='main_comments')
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    class_choice = models.CharField(max_length=30, blank=False, choices=CLASS_CHOICES) 
    upvotes     = models.IntegerField(default=0)
    downvotes   = models.IntegerField(default=0)

class CommentReply(models.Model):
    replied_to = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE, related_name='replies')
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    class_choice = models.CharField(max_length=30, blank=False, choices=CLASS_CHOICES) 
    upvotes     = models.IntegerField(default=0)
    downvotes   = models.IntegerField(default=0)

class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)