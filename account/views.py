from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.tokens import account_activation_token
from .forms import LoginForm, UserRegistrationForm
from posts.forms import PostForm
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
                    return redirect('account:profile')
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
    form = PostForm()
    context = {'display_section': 'dashboard',
               'html_title': f'{request.user} account',
               }

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
        user.save()
        login(request, user)
        return redirect('account:profile')
    else:
        return HttpResponse('Activation link is invalid')
