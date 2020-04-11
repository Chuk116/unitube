from django import forms
from .models import Video, CLASS_CHOICES

class PostForm(forms.Form):
    video_link = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'cols': 10, 'rows': 1}))
    title = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'cols': 10, 'rows': 1}))
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}))
    class_choice = forms.ChoiceField(choices=CLASS_CHOICES)
    
    class Meta:
        model = Video
        fields = ('video_link', 'title', 'description', 'class_choice')

    def clean(self):
        video_link = self.cleaned_data.get('video_link')
        cleanlink, link_or_error, video_id = cleanLink(video_link)
        if not cleanlink:
            self.add_error('video_link', link_or_error)
        else:
            video_link = link_or_error
            self.cleaned_data['video_link'] = video_link
            class_choice = self.cleaned_data.get('class_choice')
            videos = Video.objects.filter(video_id=video_id)
            if videos.exists():
                print('Video exists')
                for video in videos:
                    if video.class_choice == class_choice:
                        print('Video has error')
                        self.add_error('class_choice', 'This video has already been added for this class.')
                    else:
                        self.cleaned_data['video_id'] = video_id
                        self.cleaned_data['uni_video_id'] = video_id + randomStringDigits()
                        self.cleaned_data['embed_link'] = "https://www.youtube.com/embed/" + video_id
            else:
                self.cleaned_data['video_id'] = video_id
                self.cleaned_data['uni_video_id'] = video_id + randomStringDigits()
                self.cleaned_data['embed_link'] = "https://www.youtube.com/embed/" + video_id
            
        return self.cleaned_data

def cleanLink(video_link):
    start = 'https://youtu.be/'
    start2 = 'https://www.youtube.com/watch?v='
    error_message = 'You\'ve entered an invalid link. Please enter a valid Youtube video link.'
    lengthLink = len(video_link)
    id = ''
    
    if lengthLink <= len(start):
        return False, error_message, None
    
    beginLink = video_link[0:17].lower()
    beginLink2 = ''
    if lengthLink > len(start2):
        beginLink2 = beginLink + video_link[17:32]

    if beginLink != start and beginLink2 != start2:
        return False, error_message, None
    elif beginLink == start:
        newLink = beginLink + video_link[17:len(video_link)]
        id = video_link[17:len(video_link)]
    else:
        newLink = beginLink2 + video_link[32:len(video_link)]
        id = video_link[32:len(video_link)]

    return True, newLink, id

import random
import string

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

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

class CommentForm(forms.Form):
    message = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={
                    "style": "border:none",
                    "class": "form-control",
                    "placeholder": 'Post a comment',
                }
                
            )
    )
