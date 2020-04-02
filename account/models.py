from django.db import models
from django.contrib.auth.models import User

DEFAULT = ('', '')
LEARN_STYLES_CHOICES = [
    DEFAULT,
    ('Visual', 'Visual'),
    ('Verbal', 'Verbal'),
    ('Aural', 'Aural'),
    ('Kinesthetic', 'Kinesthetic'),
    ('Logical', 'Logical'),
]

YEAR_IN_SCHOOL_CHOICES = [
    DEFAULT,
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
    ('Graduate Student', 'Graduate Student'),
    ('Postdoc', 'Postdoc'),
    ('Not in School', 'Not in School'),
]

MAJOR_CHOICES = [
    DEFAULT,
    ('Computer Science', 'Computer Science'),
]

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_style = models.CharField(max_length=100, blank=False, choices=LEARN_STYLES_CHOICES)
    year_in_school = models.CharField(
        max_length=100,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default="Unknown",
    )
    major = models.CharField(max_length=100, blank=False, default="Unknown")
    