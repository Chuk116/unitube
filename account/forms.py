from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, LEARN_STYLES_CHOICES, YEAR_IN_SCHOOL_CHOICES, MAJOR_CHOICES

class EditProfileForm(UserChangeForm):
    learning_style = forms.TypedChoiceField(choices=LEARN_STYLES_CHOICES)
    year_in_school = forms.TypedChoiceField(choices=YEAR_IN_SCHOOL_CHOICES)
    major = forms.TypedChoiceField(choices=MAJOR_CHOICES)
    password = None

    class Meta:
        model = Profile
        fields = ('learning_style', 'year_in_school', 'major')

    # def clean(self):
    #     style = self.cleaned_data.get('learning_style')
    #     year = self.cleaned_data.get('year_in_school')
    #     major = self.cleaned_data.get('major')
    #     error = 'A selection must be made here.'
    #     if (style == ''):
    #         self.add_error('learning_style', error)
    #     if (year == ''):
    #         self.add_error('year_in_school', error)
    #     if (major == ''):
    #         self.add_error('major', error)

     #   return self.cleaned_data