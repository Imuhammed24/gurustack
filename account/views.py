from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import formats
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST

from account.models import Contact, Profile
from account.tokens import account_activation_token
from actions.models import Action
from actions.utils import create_action
from chat.models import Conversation
from chat.utils import base64_decode
from posts.forms import TagForm
from posts.models import Post, Tag
from searches.models import SearchQuery
from .forms import LoginForm, UserRegistrationForm, \
    StudentProfileForm, EditProfileForm, \
    StaffProfileForm, EditStaffProfileForm


# Create your views here.
# comment_form = CommentForm()


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
def search_view(request):
    query = request.GET.get('q', None)
    trends = Tag.tags.most_common()
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]
    user = None
    users_queryset = None
    posts_queryset = None
    if request.user.is_authenticated:
        user = request.user
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        lookup = (
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(email__icontains=query) |
                Q(last_name__icontains=query)
                )
        users_queryset = User.objects.filter(lookup)
        posts_queryset = Post.objects.search(query=query)
    context = {'display_section': 'explore',
               'html_title': f'{request.user} account',
               'users_to_follow': users,
               'trends': trends,
               'query': query,
               'users_queryset': users_queryset,
               'posts_queryset': posts_queryset}

    return render(request, 'account_base.html', context)


@login_required
def account_view(request):

    following_ids = request.user.following.values_list('id', flat=True)
    other_users_ids = User.objects.filter(is_active=True).exclude(pk=request.user.id).values_list('id', flat=True)
    not_following_ids = other_users_ids.filter(is_active=True).exclude(pk__in=following_ids).values_list('id', flat=True)

    posts = Post.objects.all().exclude(user__pk__in=not_following_ids)

    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]

    trends = Tag.tags.most_common()

    context = {'display_section': 'home',
               'html_title': f'{request.user} account',
               'tag_form': TagForm,
               'posts': posts,
               'users_to_follow': users,
               'trends': trends,
               }

    return render(request, 'account_base.html', context)


@login_required
def messages_view(request, room_name=None):
    people_messaged = []
    established_conversation = Conversation.objects.filter(participants__in=[request.user])
    for conversation in established_conversation:
        for user in conversation.participants.all():
            people_messaged.append(user.username)

    following_ids = request.user.following.values_list('id', flat=True)
    followers_ids = request.user.followers.values_list('id', flat=True)

    # get users that are not followed and are not followers
    unconnected_contacts = User.objects.filter(is_active=True)\
        .exclude(pk__in=following_ids)\
        .exclude(pk__in=followers_ids)

    # get the users someone is followers and following
    connected_users = User.objects.filter(is_active=True)\
        .exclude(pk__in=unconnected_contacts)\
        .distinct().\
        exclude(username__in=people_messaged)

    context = {'display_section': 'messages',
               'html_title': f'{request.user} Messages',
               'contacts': connected_users,
               }

    if room_name is not None:
        room_name_4_decode = base64_decode(room_name)
        extracted_timezones = room_name_4_decode.decode("utf-8")
        split_secrets = extracted_timezones.split('secnd')
        target_secret = None
        request_legitimacy = False

        for code in split_secrets:
            # parsed_date = parse(date)
            if request.user.profile.secret_code != code:
                target_secret = code
            else:
                request_legitimacy = True
        if request_legitimacy is True:
            profile = get_object_or_404(Profile, secret_code=target_secret)

            context['user'] = profile.user
            context['room_name'] = room_name

            return render(request, 'account_base.html', context)
        else:
            return redirect('account:messages')

    else:
        return render(request, 'account_base.html', context)


@login_required
def user_detail_view(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]
    no_media_posts = Post.objects.filter(user=user, images=None).values_list('id', flat=True)
    all_posts = Post.objects.filter(user=user)
    media_posts = all_posts.exclude(pk__in=no_media_posts)
    trends = Tag.tags.most_common()
    # trends = Tag.tags.all()

    context = {'display_section': 'user_detail',
               'html_title': f'{user.username} account',
               'media_posts': media_posts,
               'users_to_follow': users,
               'trends': trends,
               'user': user, }

    return render(request, 'account_base.html', context)


@login_required
def connect_view(request):
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]
    context = {'display_section': 'connect',
               'html_title': f'connect {request.user.username}',
               'users_to_follow': users, }

    return render(request, 'account_base.html', context)


@login_required
def notifications_view(request):
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]
    actions = Action.objects.all().exclude(user=request.user)
    trends = Tag.tags.most_common()
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user',
                                                                           'user__profile').prefetch_related('target')
    # actions = actions[:10]
    context = {'display_section': 'notifications',
               'html_title': f'{request.user.username}_Notifications',
               'users_to_follow': users,
               'trends': trends,
               'actions': actions, }

    return render(request, 'account_base.html', context)


@login_required
def profile_view(request):
    following_ids = request.user.following.values_list('id', flat=True)
    users = User.objects.filter(is_active=True).exclude(pk__in=following_ids).exclude(username=request.user.username).order_by('?')[:5]
    trends = Tag.tags.most_common()
    profile_form = StudentProfileForm()
    staff_profile_form = StaffProfileForm()
    edit_profile_form = None
    if request.user.profile:
        edit_profile_form = EditProfileForm(instance=request.user.profile)
    context = {'display_section': 'profile',
               'profile_form': profile_form,
               'staff_profile_form': staff_profile_form,
               'edit_profile_form': edit_profile_form,
               'trends': trends,
               'users_to_follow': users,
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
        create_action(request.user, 'has created an account')
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

    else:
        post.users_like.add(request.user)
        if request.user is not post.user:
            create_action(request.user, 'likes', post)

    context = {'post': post}
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


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('user_id')
    user = get_object_or_404(User, id=user_id, is_active=True)

    if user.followers.filter(id=request.user.id).exists():
        Contact.objects.filter(user_from=request.user,
                               user_to=user).delete()
        # create_action(request.user, 'is following', user)
        is_followed = False
    else:
        Contact.objects.get_or_create(user_from=request.user,
                                      user_to=user)
        create_action(request.user, 'started following', user)
        is_followed = True

    context = {'user': user,
               'is_followed': is_followed,
               'total_no_followers': user.followers.count,
               'all_followers': user.followers.all,
               'total_no_following': user.following.count,
               }

    if request.is_ajax():
        html = render_to_string('account/user/follow-unfollow-form.html', context, request=request)
        return JsonResponse({'form': html})
