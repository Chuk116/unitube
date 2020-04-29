from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import VALID_EMAIL_DOMAINS

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',
            'password1', 'password2', )
        


    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email is not None:
            if not _emailDomainIsValid(email):
                self.add_error('email', 'The email is not part of a valid domain!')
            elif User.objects.filter(email=email).exists():
                self.add_error('email', "This email is already in use!")
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'This username is already in use!')
        return self.cleaned_data

def _emailDomainIsValid(email):
    return email.split('@')[1] in VALID_EMAIL_DOMAINS
        

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ('email', 'password',)