from django.shortcuts import render
from searching.forms import SearchForm
from .forms import PostForm
from .models import Video
from cas.decorators import gateway

@gateway()
def post_video(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Video.objects.create(user=request.user, video_id=form.cleaned_data['video_id'], embed_link=form.cleaned_data['embed_link'], link=form.cleaned_data['video_link'], title=form.cleaned_data['title'], description=form.cleaned_data['description'], class_choice=form.cleaned_data['class_choice'])
            return render(request, '../templates/posting/post-video-success.html')
        else:
            # return invalid login error message
            return render(request, '../templates/posting/post-video.html', {'form': form, 'error_message': "There was an error posting the video."})
    else:
        form = PostForm()

    context = {'form':form}
    return render(request, '../templates/posting/post-video.html', context=context)

# Create your views here.
