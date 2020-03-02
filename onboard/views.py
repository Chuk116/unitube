from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
        else:
          error_message=''
          username = request.POST['username']
          try:
            user = User.objects.get(username=username)
          except:
            error_message = "We encountered a problem signing you up"
          return render(request, 'registration/signup.html', {'form': form, 'error_message':error_message})

    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})
