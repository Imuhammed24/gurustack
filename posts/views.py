from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .forms import PostForm, TagForm
from .models import Post


@login_required()
def create_post(request):
    # image_form_set = modelformset_factory(Post, fields=('image', ), extra=5)
    if request.method == 'POST':
        # formset = image_form_set(data=request.POST or None,  files=request.FILES or None)
        print('check post')
        if request.FILES.get('image') or request.POST.get('article'):
            post = Post()
            post.article = request.POST.get('article')
            # post.image = request.FILES.get('image')
            # for image in request.FILES.getlist('image'):
            #     post.image = image
            #     post.save()
            post.user = request.user
            post.save()

            messages.success(request, 'Posted!')

            tag_form = TagForm(data=request.POST)
            if tag_form.is_valid():
                form = tag_form.save(commit=False)
                form.post = post
                form.save()
                tag_form.save_m2m()
            # print([tag for tag in post.tag])
            return redirect('account:profile')

    return redirect('account:profile')
