from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    article = forms.CharField(widget=forms.Textarea, max_length=400)

    class Meta:
        model = Post
        fields = ['article', 'image']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tags']
