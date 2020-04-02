from django.shortcuts import render, redirect
from .forms import EditProfileForm

# Create your views here.
def view_profile(request):
    return render(request, "account/profile_page.html")

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
        else:
            form = EditProfileForm(instance=request.user.profile)
            form['learning_style'].label = 'Which best describes your learning style?'
            return render(request, 'account/edit_profile.html')
    else:
        form = EditProfileForm(instance=request.user.profile)
        form['learning_style'].label = 'Which best describes your learning style?'
        return render(request, 'account/edit_profile.html', {'form':form})