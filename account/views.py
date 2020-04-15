from django.shortcuts import render, redirect
from .forms import EditProfileForm
from videos.forms import SearchForm

# Create your views here.
def view_profile(request):
    query = request.session['query']
    class_ = request.session['class_']
    initial = {
        'search': query,
        'class_': class_,
    }
    searchForm = SearchForm(initial=initial)
    context = {'searchForm': searchForm}
    return render(request, "account/profile_page.html", context=context)

def edit_profile(request):
    query = request.session['query']
    class_ = request.session['class_']
    initial = {
        'search': query,
        'class_': class_,
    }
    searchForm = SearchForm(initial=initial)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
        else:
            form = EditProfileForm(instance=request.user.profile)
            form['learning_style'].label = 'Which best describes your learning style?'
            return render(request, 'account/edit_profile.html', {'searchForm':searchForm})
    else:
        form = EditProfileForm(instance=request.user.profile)
        form['learning_style'].label = 'Which best describes your learning style?'
        return render(request, 'account/edit_profile.html', {'form':form, 'searchForm':searchForm})