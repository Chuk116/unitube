from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
from django.core.mail import EmailMessage


from .forms import SignUpForm, LoginForm
from account.forms import EditProfileForm
from videos.forms import SearchForm
from account.models import Profile
from videos.models import SearchFilters, ClassFilters

def signup(request):
    if request.method == 'POST':
        formUser = SignUpForm(request.POST)
        formProf = EditProfileForm(request.POST)
        if formUser.is_valid() and formProf.is_valid():
            user = formUser.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Unitube account!'
            message = render_to_string('onboard/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = formUser.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            Profile.objects.create(user=user, learning_style=formProf.cleaned_data['learning_style'], year_in_school=formProf.cleaned_data['year_in_school'],major=formProf.cleaned_data['major'])
            # return HttpResponse('Please confirm your email address to complete the registration')
            return render(request, "onboard/acc_active_email_sent.html")
        else:
          error_message=''
          username = request.POST['username']
          try:
            user = User.objects.get(username=username)
          except:
            error_message = "We encountered a problem signing you up"
          return render(request, 'onboard/signup.html', {'formUser': formUser, 'formProf': formProf, 'error_message':error_message})
        
        return render(request, 'onboard/signup_confirmed.html')

    else:
        formUser = SignUpForm()
        formProf = EditProfileForm()
        formProf['learning_style'].label = 'Which best describes your learning style?'
        return render(request, 'onboard/signup.html', {'formUser': formUser, 'formProf':formProf})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
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
                context = {'query': '',}
                return redirect('home')
            else:
                # return invalid login error message
                return render(request, '../templates/login.html', {'form': form, 'error_message': "Incorrect username and/or password"})
    else:
        form = LoginForm()
    
    context = {'form': form,}
    return render(request, '../templates/login.html', context=context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        SearchFilters.objects.create(user=user)
        ClassFilters.objects.create(user=user)
        # auth_login(request, user)
        # return redirect('home')
        return render(request, 'onboard/acc_active_confirm_landing.html')
    else:
        return render(request, 'onboard/acc_active_reject_landing.html')

def home(request):
    if 'query' in request.session:
        query = request.session['query']
    else:
        query = ''
    context = {'query': query}
    return render(request, '../templates/homepage.html', context=context)

def logout(request):
    auth_logout(request)
    return redirect('home')
