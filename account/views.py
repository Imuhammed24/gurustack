import json

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import formats
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST
from django.views.generic import FormView

from account.tokens import account_activation_token
from posts.forms import TagForm, ImageForm, CommentForm
from posts.models import Post
from .forms import LoginForm, UserRegistrationForm, \
    StudentProfileForm, EditProfileForm, \
    StaffProfileForm, EditStaffProfileForm


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account:home')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm
    return render(request, 'registration/login.html', {'html_title': 'Gurustack_Login',
                                                       'form': form})


@login_required
def account_view(request):
    image_form = ImageForm()
    comment_form = CommentForm()
    posts = Post.objects.all()

    context = {'display_section': 'home',
               'html_title': f'{request.user} account',
               'tag_form': TagForm,
               'image_form': image_form,
               'posts': posts,
               'comment_form': comment_form,
               # 'total_no_likes': post.users_like.count,
               }

    return render(request, 'account_base.html', context)


@login_required
def profile_view(request):
    comment_form = CommentForm()
    profile_form = StudentProfileForm()
    staff_profile_form = StaffProfileForm()
    edit_profile_form = None
    if request.user.profile:
        edit_profile_form = EditProfileForm(instance=request.user.profile)
    context = {'display_section': 'profile',
               'profile_form': profile_form,
               'staff_profile_form': staff_profile_form,
               'edit_profile_form': edit_profile_form,
               'comment_form': comment_form,
               'html_title': f'{request.user} profile',
               }
    if request.user.profile.staff_status:
        edit_staff_profile_form = EditStaffProfileForm(instance=request.user.profile)
        context['edit_staff_profile_form'] = edit_staff_profile_form
    request.user.date_joined = formats.date_format(request.user.date_joined, "DATE_FORMAT")
    return render(request, 'account_base.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.is_active = False
            new_user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Gurustack Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            new_user.email_user(subject, message)
            messages.success(request, 'Please confirm your email to complete registration')

            form = LoginForm

            return render(request, 'registration/login.html', {'html_title': 'Gurustack_Login',
                                                               'form': form})

        else:
            messages.error(request, f'{user_form.errors}')
            return redirect('account:register')
            # raise user_form.errors

    else:
        form = UserRegistrationForm()
        return render(request, 'account/register.html', {'html_title': 'Join Gurustack Now',
                                                         'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('account:home')
    else:
        return HttpResponse('Activation link is invalid')


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.users_like.filter(id=request.user.id).exists():
        post.users_like.remove(request.user)
        # post.is_liked = False
        # post.total_no_likes = post.users_like.count

    else:
        post.users_like.add(request.user)
        # post.is_liked = True
        # post.total_no_likes = post.users_like.count

    context = {'post': post,
               # 'is_liked': post.is_liked,
               # 'total_no_likes': post.users_like.count,
               }
    if request.is_ajax():
        html = render_to_string('posts/like_section.html', context, request=request)
        return JsonResponse({'form': html})


@login_required
@require_POST
def edit_profile_view(request):
    edit_profile_form = StudentProfileForm(instance=request.user.profile,
                                           data=request.POST,
                                           files=request.FILES)
    edit_staff_profile_form = EditStaffProfileForm(instance=request.user.profile,
                                                   data=request.POST,
                                                   files=request.FILES)
    if edit_profile_form is not None:
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Profile edited successfully')
        else:
            messages.error(request, 'Error editing profile')

    if edit_staff_profile_form is not None:
        if edit_staff_profile_form.is_valid():
            edit_staff_profile_form.save()
            messages.success(request, 'Profile edited successfully')
        else:
            messages.error(request, 'Error editing profile')
    return redirect('account:profile')


@login_required
@require_POST
def register_profile_view(request):
    profile_form = StudentProfileForm(instance=request.user.profile,
                                      data=request.POST or None,
                                      files=request.FILES or None)
    staff_profile_form = StaffProfileForm(instance=request.user.profile,
                                          data=request.POST or None,
                                          files=request.FILES or None)
    if profile_form is not None:
        if profile_form.is_valid():
            obj = profile_form.save(commit=False)
            obj.save()
            messages.success(request, 'Profile created successfully')
        else:
            messages.error(request, 'Error creating profile')

    if staff_profile_form is not None:
        if staff_profile_form.is_valid():
            profile = staff_profile_form.save(commit=False)
            profile.staff_status = True
            profile.verified = True
            profile.save()
            messages.success(request, 'Profile created successfully')
        else:
            messages.error(request, 'Error creating profile')
    return redirect('account:profile')


class AutoCompleteView(FormView):
    def get(self, request, *args):
        data = request.GET
        username = data.get("term")
        if username:
            users = User.objects.filter(username__icontains=username)
        else:
            users = User.objects.all()
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            results.append(user_json)
            data = json.dumps(results)
            mimetype = 'application/json'
        return HttpResponse(data, mimetype)
