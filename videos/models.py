from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from account.models import LEARN_STYLES_CHOICES

CLASS_CHOICES = [
    ('General','General'),
    ('Cos109', 'Cos109'),
    ('Cos126', 'Cos126'),
    ('Cos217', 'Cos217'),
    ('Cos226', 'Cos226'),
    ('Cos306', 'Cos306'),
    ('Cos314', 'Cos314'),
    ('Cos315', 'Cos315'),
    ('Cos320', 'Cos320'),
    ('Cos333', 'Cos333'),
    ('Cos340', 'Cos340'),
    ('Cos424', 'Cos424'),
]

TIME_LENGTH_CHOICES = [
    ('short', 'Short (0 - 5 minutes)'),
    ('medium', 'Medium (5 - 15 minutes)'),
    ('semi-long', 'Semi-Long (15 - 25 minutes)'),
    ('long', 'Long (25+ minutes)'),
]

SORT_BY_CHOICES = [
    ('Relevance', 'Relevance'),
    ('TimeS', 'Shortest Time'),
    ('Approval', 'Approval (Rating/Likes)'),
    ('Views', 'Most Views'),
    ('Comments', 'Most Comments'),
    ('TimeL', 'Longest Time')
]

SORT_BY_DATA_CHOICES = [
    ('Unitube', 'Unitube Data'),
    ('Youtube', 'Youtube Data'),
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
    time_length = models.IntegerField(default=0)
    time_length_str = models.TextField(default='00:00:00')
    num_views = models.IntegerField(default=0)
    num_likes = models.IntegerField(default=0)
    num_dislikes = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    tags = models.CharField(max_length=3000, blank=True)
    thumbnail_link = models.TextField(default='', blank=True)

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

class SearchFilters(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_style = models.CharField(default='', max_length=3000, choices=LEARN_STYLES_CHOICES)
    time_length = MultiSelectField(default='', choices=TIME_LENGTH_CHOICES)
    sort_by = models.CharField(default='Relevance', max_length=3000, choices=SORT_BY_CHOICES)
    sort_using = models.CharField(max_length=3000, default='Unitube', choices=SORT_BY_DATA_CHOICES)

class ClassFilters(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes = MultiSelectField(default='General', choices=CLASS_CHOICES)