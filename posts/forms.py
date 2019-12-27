from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    article = forms.CharField(widget=forms.Textarea, max_length=400)

    class Meta:
        model = Post
        fields = ['article', 'image', 'tags']
