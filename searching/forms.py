from django import forms
from posting.models import Video, CLASS_CHOICES

class SearchForm(forms.Form):
    search = forms.CharField(
            required=False,
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": 'Search',
                }
                
                )
    )
    class_ = forms.ChoiceField(choices=CLASS_CHOICES)
    
    class Meta:
        fields = ('search', 'class_')