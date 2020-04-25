from django.shortcuts import render, redirect
from .forms import EditProfileForm
from videos.forms import SearchForm
from videos.views import _getSearchCookies
from django.contrib.auth.models import User

# Create your views here.
def my_profile(request):
    query = _getSearchCookies(request)
    context = {'query': query}
    return render(request, "account/profile_page.html", context=context)

def edit_profile(request):
    query = _getSearchCookies(request)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        else:
            form = EditProfileForm(instance=request.user.profile)
            form['learning_style'].label = 'Which best describes your learning style?'
            return render(request, 'account/edit_profile.html', {'query':query})
    else:
        form = EditProfileForm(instance=request.user.profile)
        form['learning_style'].label = 'Which best describes your learning style?'
        return render(request, 'account/edit_profile.html', {'form':form, 'query':query})

def view_profile(request, **kwargs):
    query = _getSearchCookies(request)
    username = kwargs.get('username')
    user = User.objects.filter(username=username)
    user = user[0]
    return render(request, 'account/view_profile.html', {'target_user':user, 'query':query})
