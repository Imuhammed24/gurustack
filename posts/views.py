from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from .forms import ImageForm, TagForm, CommentForm
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
            return redirect('account:home')
    return


# @login_required
# @require_POST
# def post_like(request):
#     post_id = request.POST.get('post_id')
#     post = get_object_or_404(Post, id=post_id)
#     if post.users_like.filter(id=request.user.id).exists():
#         post.users_like.remove(request.user)
#         is_liked = False
#     else:
#         post.users_like.add(request.user)
#         is_liked = True
#
#     context = {'post': post,
#                'is_liked': is_liked,
#                'total_no_likes': post.users_like.count,
#                'users_like': post.users_like.all}
#     if request.is_ajax():
#         html = render_to_string('like_section.html', context, request=request)
#         return JsonResponse({'form': html})
