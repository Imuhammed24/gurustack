from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post


@login_required()
def create_post(request):
    if request.method == 'POST':
        print('check post')
        if request.FILES.get('image') or request.POST.get('article'):
            print('check condition')
            post = Post()
            print('create obj')
            post.article = request.POST.get('article')
            print('create article')
            post.tags = request.POST.get('tags')
            print('create tags')
            post.image = request.FILES.get('image')
            print('create img')
            post.user = request.user
            post.save()
            messages.success(request, 'Posted!')
            return redirect('account:profile')

        # print('posted')
        # form = PostForm(data=request.POST, files=request.FILES)
        # if form.is_valid():
        #     new_item = form.save(commit=False)
        #     new_item.user = request.user
        #     new_item.save()
        #     messages.success(request, 'Posted!')
        #     return redirect('account:profile')

    else:
        form = PostForm()
    return redirect('account:profile')
