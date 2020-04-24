from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# from cas.decorators import gateway
from .forms import SearchForm, PostForm, CommentForm, SearchFilterForm
from .search import search_videos
from .models import Video, CommentThread, Comment, Rating, YoutubeData, SearchFilters
from uniauth.decorators import login_required as cas_login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q
from unitube.settings import YOUTUBE_API_KEY
import urllib.request
import json

# @gateway()
def search(request):
    searchForm = SearchForm()
    filterForm = SearchFilterForm(initial={'sort_using': 'Unitube', 'sort_by':'Relevance'})
    filters = []
    if request.user.is_authenticated:
        filters = _getSearchFilters(request.user)
        initial_data = {
            "learning_style": filters[0],
            "time_length": filters[1],
            "sort_by": filters[2],
            "sort_using": filters[3],
        }
        filterForm = SearchFilterForm(initial=initial_data)
    else:
        filters = ['', [], 'Relevance', 'Unitube']

    context = {'searchForm': searchForm, 'filterForm': filterForm}
    
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        searchquery = ''
        class_selection = ''
        if searchForm.is_valid():
            # searchForm.save()
            searchquery = request.POST.get('search')
            class_choice = request.POST.get('class_')

        videolist = search_videos(searchquery, class_choice, filters)
            
        context['videolist'] = videolist
        context['searchForm'] = searchForm


        request.session['query'] = searchquery
        request.session['class_'] = class_choice

    return render(request, '../templates/viewing/videos-list.html', context=context)

def filter_search(request, **kwargs):
    searchForm, query, class_choice = _getSearchCookies(request)
    context = {
        'searchForm': searchForm,
    }

    if request.method == 'POST':
        filterForm = SearchFilterForm()
        learn_style = request.POST.get('learning_style')
        learn_style = '' if learn_style is None else learn_style
        time_length = request.POST.getlist('time_length')
        sort_by = request.POST.get('sort_by')
        sort_by = '' if sort_by is None else sort_by
        sort_using = request.POST.get('sort_using')
        sort_using = 'Unitube' if sort_using is None else sort_using
        filters = [learn_style, time_length, sort_by, sort_using]

        context['filterForm'] = filterForm
        videolist = search_videos(query, class_choice, filters)

        if kwargs.get('s') == 1:
            SearchFilters.objects.filter(user=request.user).update(learning_style=learn_style, time_length=time_length, sort_by=sort_by, sort_using=sort_using)
        
        context['videolist'] = videolist
    
    if request.user.is_authenticated:
        filters = _getSearchFilters(request.user)
        initial_data = {
            "learning_style": filters[0],
            "time_length": filters[1],
            "sort_by": filters[2],
            "sort_using": filters[3],
        }
        filterForm = SearchFilterForm(initial=initial_data)
    else:
        filterForm = SearchFilterForm(initial={'sort_using':'Unitube', 'sort_by': 'Relevance'})

        

    context['filterForm'] = filterForm

    return render(request, '../templates/viewing/videos-list.html', context=context)

def post_video(request):
    if request.user.is_authenticated:
        searchForm, _, _ = _getSearchCookies(request)

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                video = Video.objects.create(user=request.user, video_id=form.cleaned_data['video_id'], uni_video_id=form.cleaned_data['uni_video_id'],
                    embed_link=form.cleaned_data['embed_link'], link=form.cleaned_data['video_link'], 
                    title=form.cleaned_data['title'], description=form.cleaned_data['description'], class_choice=form.cleaned_data['class_choice'])
                CommentThread.objects.create(video=video)
                _storeYoutubeData(video, form.cleaned_data['snippet_data'])
                context = {'searchForm': searchForm}
                return render(request, '../templates/posting/post-video-success.html', context=context)
            else:
                context = {
                    'form': form,
                    'error_message': "There was an error posting the video.",
                    'searchForm': searchForm,
                }
                # return invalid login error message
                return render(request, '../templates/posting/post-video.html', context=context)
        else:
            form = PostForm()

        context = {'form':form, 'searchForm':searchForm}
        return render(request, '../templates/posting/post-video.html', context=context)
    else:
        return redirect('home')

def video_page(request, **kwargs):
    uni_video_id = kwargs.get('video_id')
    video = Video.objects.get(uni_video_id=uni_video_id)
    searchForm, _, _ = _getSearchCookies(request)
    rating = 0
    if request.user.is_authenticated:
        rating_obj_list = Rating.objects.filter(Q(video=video), Q(user=request.user))
        rating = 0 if len(rating_obj_list) == 0 else rating_obj_list[0].rating

    commentForm = CommentForm()

    context = {
        'video': video,
        'searchForm': searchForm,
        'commentForm': commentForm,
        'rating': rating
    }
    #request.session['v'] = uni_video_id
    return render(request, 'viewing/video-page.html', context=context)

def post_comment(request):
    if request.method == 'POST':
        cmtText = request.POST['comment']
        uni_video_id = request.POST['uni_video_id']
        thread_pk = request.POST['thread_pk']
        class_ = request.POST['class_']
        thread = get_object_or_404(CommentThread, pk=int(thread_pk))
        comment = Comment.objects.create(thread=thread, user=request.user, message=cmtText, class_choice=class_)
        thread.num_comments += 1
        thread.save()
        return_data = {
            'num_comments': int(thread.num_comments),
            'timestamp': str(comment.timestamp)
        }
        return HttpResponse(json.dumps(return_data))

def post_rating(request):
    if request.method == 'POST':
        new_rating = request.POST['rating']
        uni_video_id = request.POST['uni_video_id']
        video = Video.objects.get(uni_video_id=uni_video_id)
        
        rating_obj = Rating.objects.filter(Q(video=video), Q(user=request.user))
        if len(rating_obj) == 0:
            rating_obj = Rating.objects.create(video=video, user=request.user, rating=new_rating)
            video.num_ratings += 1
            newAvg = (video.avg_rating * video.num_ratings + int(new_rating)) / (video.num_ratings)
        else:
            newAvg = (video.avg_rating * video.num_ratings - rating_obj[0].rating + int(new_rating)) / video.num_ratings
            rating_obj[0].rating = new_rating
            rating_obj[0].save()

        video.avg_rating = newAvg
        video.save()

        return HttpResponse('')

# Stores the fetched youtube data for the specific video into the database
def _storeYoutubeData(video, snippet_data):
    video_id = video.video_id
    url_content = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
    content_data = json.loads(urllib.request.urlopen(url_content).read())['items'][0]['contentDetails']
    url_stats = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    stats_data =  json.loads(urllib.request.urlopen(url_stats).read())['items'][0]['statistics']

    tags = ''
    if 'tags' in snippet_data:
        for tag in snippet_data['tags']:
            tags += tag + ','

    if 'defaultAudioLanguage' in snippet_data:
        lang = snippet_data['defaultAudioLanguage']
    else:
        lang = 'N/A'
    
    time_length_str = content_data['duration'][2:len(content_data['duration'])]
    time_length = 0
    if 'H' in time_length_str:
        tl_H = time_length_str.split('H')
        tl_M = tl_H[1].split('M')
        tl_S = tl_M[1].split('S')
    elif 'M' in time_length_str:
        tl_H = [0]
        tl_M = time_length_str.split('M')
        tl_S = tl_M[1].split('S')
    else:
        tl_H = [0]
        tl_M = [0]
        tl_S = time_length_str.split('S')

    time_length = int(tl_H[0]) * 3600 + int(tl_M[0]) * 60 + int(tl_S[0])

    YoutubeData.objects.create(video=video,title=snippet_data['title'],description=snippet_data['description'],lang=lang,
    time_length=time_length,num_views=int(stats_data['viewCount']),num_likes=int(stats_data['likeCount']),num_dislikes=int(stats_data['dislikeCount']),
    num_comments=int(stats_data['commentCount']), tags=tags, thumbnail_link=snippet_data['thumbnails']['high']['url'])

def _getSearchFilters(user):
    searchFilter = SearchFilters.objects.get(user=user)
    filters = [searchFilter.learning_style, searchFilter.time_length, searchFilter.sort_by, searchFilter.sort_using]
    return filters

def _getSearchCookies(request):
    if 'query' in request.session:
        query = request.session['query']
        class_ = request.session['class_']
        initial = {
            'search': query,
            'class_': class_,
        }
        return SearchForm(initial=initial), query, class_
    else:
        return SearchForm(), '', 'All'
