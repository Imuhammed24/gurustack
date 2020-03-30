from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import login_view, register, account_view, activate, post_like, profile_view, edit_profile_view, \
    register_profile_view, user_follow, connect_view, notifications_view

urlpatterns = [
    path('notifications/', notifications_view, name='notifications'),
    path('login/', login_view, name='login'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like-post/', post_like, name='like-post'),
    path('connect/', connect_view, name='connect'),
    path('profile/', profile_view, name='profile'),
    path('register-profile/', register_profile_view, name='register_profile'),
    path('home/', account_view, name='home'),
    path('follow/', user_follow, name='user-follow'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url=reverse_lazy('account:password_change_done')), name='password_change'),

    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
