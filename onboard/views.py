from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


from .forms import SignUpForm, LoginForm
from account.forms import EditProfileForm
from searching.forms import SearchForm
from account.models import Profile

def signup(request):
    if request.method == 'POST':
        formUser = SignUpForm(request.POST)
        formProf = EditProfileForm(request.POST)
        if formUser.is_valid() and formProf.is_valid():
            user = formUser.save()
            Profile.objects.create(user=user, learning_style=formProf.cleaned_data['learning_style'], year_in_school=formProf.cleaned_data['year_in_school'],major=formProf.cleaned_data['major'])
        else:
          error_message=''
          username = request.POST['username']
          try:
            user = User.objects.get(username=username)
          except:
            error_message = "We encountered a problem signing you up"
          return render(request, 'registration/signup.html', {'formUser': formUser, 'formProf': formProf, 'error_message':error_message})
        
        return render(request, 'registration/signup_confirmed.html')

    else:
        formUser = SignUpForm()
        formProf = EditProfileForm()
        formProf['learning_style'].label = 'Which best describes your learning style?'
        return render(request, 'registration/signup.html', {'formUser': formUser, 'formProf':formProf})


def login(request):
    searchForm = SearchForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.filter(email=email)
            username = user[0].username
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                context = {'searchForm': searchForm,}
                # return redirect('admin/login')
                return render(request, '../templates/home.html', context=context)
            else:
                # return invalid login error message
                return render(request, '../templates/home.html', {'form': form, 'error_message': "Incorrect username and/or password"})
    else:
        form = LoginForm()
    
    context = {'searchForm': searchForm,
    'form': form,}
    return render(request, '../templates/home.html', context=context)

def logout(request):
    auth_logout(request)
    return redirect('home')
