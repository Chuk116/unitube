from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',
            'password1', 'password2', )

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        userEmail = User.objects.filter(email=email)
        userName = User.objects.filter(username=username)
        if userEmail:
            self.add_error('email', "This email is already in use!")
        if userName:
            self.add_error('username', 'Username is already in use')
        return self.cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = ('email', 'password',)