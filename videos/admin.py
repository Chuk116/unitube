from django.contrib import admin
from .models import Video, CommentThread, Comment, CommentReply
# Register your models here.

admin.site.register(Video)
admin.site.register(CommentThread)
admin.site.register(Comment)
admin.site.register(CommentReply)