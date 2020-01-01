from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .forms import ImageForm, TagForm
from .models import Post, Images


@login_required()
def create_post(request):
    if request.method == 'POST':
        print('check post')

        if request.FILES.get('image') or request.POST.get('article'):
            post = Post()
            post.article = request.POST.get('article')
            post.user = request.user
            post.save()

            files = request.FILES.getlist('image')
            for f in files:
                gallery = Images(post=post, image=f)
                gallery.save()

            messages.success(request, 'Posted!')

            tag_form = TagForm(data=request.POST)
            if tag_form.is_valid():
                form = tag_form.save(commit=False)
                form.post = post
                form.save()
                tag_form.save_m2m()

            return redirect('account:profile')

    return redirect('account:profile')
