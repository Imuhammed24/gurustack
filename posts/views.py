from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from actions.utils import create_action
from .forms import TagForm, CommentForm
from .models import Post, Images


@login_required
def create_post(request):
    if request.method == 'POST':
        print('check post')

        if request.FILES.get('image') != '' or request.POST.get('article') != '':
            post = Post()
            post.article = request.POST.get('article')
            post.user = request.user
            post.save()
            create_action(request.user, 'added', post)

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

            return redirect('account:home')

    return redirect('account:home')


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            obj = comment_form.save(commit=False)
            post = Post.objects.get(id=pk)
            obj.post = post
            obj.user = request.user
            obj.save()
            if request.user is not post.user:
                create_action(request.user, 'commented on', post)
            return redirect('account:home')
    return
