from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render

from actions.utils import create_action
from .forms import TagForm, CommentForm
from .models import Post, Images, Tag

comment_form = CommentForm()


@login_required
def create_post(request):
    if request.method == 'POST':
        print('check post')

        if request.FILES.getlist('image') is not None or request.POST.get('article') is not None:
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


@login_required
def post_detail_view(request, i_d, slug):
    post = get_object_or_404(Post, id=i_d, slug=slug)
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids)[:5]
    trends = Tag.tags.most_common()

    context = {'post': post,
               'display_section': 'post_detail',
               'html_title': f'{request.user} account',
               'comment_form': comment_form,
               'users_to_follow': users,
               'trends': trends,
               }

    return render(request, 'account_base.html', context)
