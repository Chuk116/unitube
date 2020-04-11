from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# from cas.decorators import gateway
from .forms import SearchForm, PostForm, CommentForm
from .search import search_videos
from .models import Video, CommentThread, Comment
from uniauth.decorators import login_required as cas_login_required
from django.views.decorators.csrf import csrf_exempt
import json
# @gateway()
def search(request):
    searchForm = SearchForm()
    context = {'searchForm': searchForm}
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        searchquery = ''
        class_selection = ''
        if searchForm.is_valid():
            # searchForm.save()
            searchquery = request.POST.get('search')
            class_choice = request.POST.get('class_')

        videolist = search_videos(searchquery, class_choice)
        context = {
            'videolist': videolist,
            'searchForm': searchForm,
        }

        request.session['query'] = searchquery
        request.session['class_'] = class_choice

    return render(request, '../templates/viewing/videos-list.html', context=context)

@cas_login_required
def post_video(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            video = Video.objects.create(user=request.user, video_id=form.cleaned_data['video_id'], uni_video_id=form.cleaned_data['uni_video_id'],
                embed_link=form.cleaned_data['embed_link'], link=form.cleaned_data['video_link'], 
                title=form.cleaned_data['title'], description=form.cleaned_data['description'], class_choice=form.cleaned_data['class_choice'])
            CommentThread.objects.create(video=video)
            return render(request, '../templates/posting/post-video-success.html')
        else:
            # return invalid login error message
            return render(request, '../templates/posting/post-video.html', {'form': form, 'error_message': "There was an error posting the video."})
    else:
        form = PostForm()

    context = {'form':form}
    return render(request, '../templates/posting/post-video.html', context=context)

def video_page(request, **kwargs):
    uni_video_id = kwargs.get('video_id')
    video = Video.objects.get(uni_video_id=uni_video_id)
    query = request.session['query']
    class_ = request.session['class_']

    initial = {
        'search': query,
        'class_': class_,
    }
    searchForm = SearchForm(initial=initial)
    commentForm = CommentForm()

    context = {
        'video': video,
        'searchForm': searchForm,
        'commentForm': commentForm,
    }
    #request.session['v'] = uni_video_id
    return render(request, 'viewing/video-page.html', context=context)

@csrf_exempt
def post_comment(request):
    print('Got here')
    if request.method == 'POST':
        print(request.POST['comment'])
        print(request.POST)
        loaded_data = json.loads(request.POST)
        cmtText = loaded_data.get('comment')
        uni_video_id = loaded_data.get('uni_video_id')
        thread_pk = loaded_data.get('thread_pk')
        class_ = loaded_data.get('class_')
        print('%s, %s, %s', cmtText, uni_video_id, thread_pk)
        thread = get_object_or_404(CommentThread, pk=int(thread_pk))
        Comment.objects.create(thread=thread, user=request.user, message=cmtText, class_choice=class_)
        print('Success')
    
    return
