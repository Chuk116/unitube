from django.shortcuts import render, redirect
from posting.models import Video
from django.contrib.auth.models import User
from cas.decorators import gateway
from searching.forms import SearchForm
from .search import search_videos

@gateway()
def search(request):
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
        return render(request, '../templates/viewing/videos-list.html', context=context)

    searchForm = SearchForm()
    context = {'searchForm': searchForm}
    return render(request, '../templates/homepage.html', context=context)

# Create your views here.
# def search(request):
#     searchForm = SearchForm()
#     if request.POST
#     videolist = Video.objects.all()
#     context = {
#         'videolist': videolist,
#         'searchForm': searchForm,
#     }
#     return render(request, '../templates/viewing/videos-list.html', context=context)