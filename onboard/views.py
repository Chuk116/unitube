from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from cas.decorators import gateway

from .forms import SignUpForm, LoginForm
from searching.forms import SearchForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
          error_message=''
          username = request.POST['username']
          try:
            user = User.objects.get(username=username)
          except:
            error_message = "We encountered a problem signing you up"
          return render(request, 'registration/signup.html', {'form': form, 'error_message':error_message})
        
        return render(request, 'registration/signup_confirmed.html')

    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

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
