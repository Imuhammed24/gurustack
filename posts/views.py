import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from actions.utils import create_action
from .forms import TagForm, CommentForm, ImageForm
from .models import Post, Images, Tag

comment_form = CommentForm()


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@login_required
def create_post(request):
    if request.method == 'POST':
        print('check post')

        files = request.FILES.getlist('image')
        if len(files) >= 1 or request.POST.get('article') != '':
            post = Post()
            if request.POST.get('article') != '':
                post.article = request.POST.get('article')
            else:
                post.slug = slugify(random_string_generator())
            post.user = request.user
            post = post.save()
            create_action(request.user, 'added', post)

            if len(files) >= 1:
                # files = request.FILES.getlist('image')
                for f in files:
                    gallery = Images(post=post, image=f)
                    gallery.save()
            else:
                print('no img')

            tag_form = TagForm(data=request.POST)
            if tag_form:
                if tag_form.is_valid():
                    form = tag_form.save(commit=False)
                    form.post = post
                    form.save()
                    tag_form.save_m2m()

            messages.success(request, 'Posted!')

            return redirect('account:home')

    return redirect('account:home')


@login_required
@require_POST
def edit_post_view(request, pk):
    post = Post.objects.get(pk=pk)

    tagform = TagForm(instance=post.tag,
                      data=request.POST,
                      files=request.FILES)

    image_form = ImageForm(instance=post.images,
                           data=request.POST,
                           files=request.FILES)

    if tagform is not None:
        if tagform.is_valid():
            tagform.save()
            messages.success(request, 'Profile edited successfully')
        else:
            messages.error(request, 'Error editing profile')

    if image_form is not None:
        if image_form.is_valid():
            image_form.save()
            messages.success(request, 'Edited successfully')
        else:
            messages.error(request, 'Error editing post')
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
            return redirect('posts:detail', i_d=post.id, slug=post.slug)
    return


@login_required
def post_detail_view(request, i_d, slug):
    post = get_object_or_404(Post, id=i_d, slug=slug)
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids)[:5]
    trends = Tag.tags.most_common()
    # edit_tags_form = TagForm(instance=post.tag)
    edit_image_form = ''

    context = {'post': post,
               'display_section': 'post_detail',
               'edit_image_form': edit_image_form,
               # 'edit_tags_form': edit_tags_form,
               'html_title': f'{request.user} account',
               'comment_form': comment_form,
               'users_to_follow': users,
               'trends': trends,
               }

    return render(request, 'account_base.html', context)
