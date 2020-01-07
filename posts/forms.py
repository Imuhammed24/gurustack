from django import forms
from .models import Post, Tag, Images, Comment


class PostForm(forms.ModelForm):
    article = forms.CharField(widget=forms.Textarea, max_length=400)

    class Meta:
        model = Post
        fields = ['article']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tags']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='', widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                   'hidden': True,
                                                                   'onchange': "loadFile(event);",
                                                                   'id': 'image',
                                                                   'accept': 'image/gif, image/jpeg, image/jpg, image/png'}))

    class Meta:
        model = Images
        fields = ['image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='',
                              widget=forms.Textarea(attrs={'placeholder': 'Type your response', 'rows': '1'}))

    class Meta:
        model = Comment
        fields = ['content']
