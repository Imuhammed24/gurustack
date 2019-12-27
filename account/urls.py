from django.urls import path, reverse_lazy
from .views import login_view, register, account_view, activate
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', account_view, name='profile'),

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
