from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    login_view,
    profile_view,
    logout_view,
    VerifyEmailView,
    VerifyEmailDoneView,
    VerifyEmailConfirmView,
    VerifyEmailCompleteView,
    check_verification_status
)

app_name = 'accounts'

urlpatterns = [
    # Основні URL для акаунтів
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

    # Скидання пароля
    path('password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            email_template_name='accounts/password_reset_email.html',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url=reverse_lazy('accounts:password_reset_done'),
            html_email_template_name='accounts/password_reset_email.html',
        ),
        name='password_reset'),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'),

    # Підтвердження email
    path('verify-email/',
        VerifyEmailView.as_view(),
        name='verify_email'),
    path('verify-email/done/',
        VerifyEmailDoneView.as_view(),
        name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/',
        VerifyEmailConfirmView.as_view(),
        name='verify_email_confirm'),
    path('verify-email/complete/',
        VerifyEmailCompleteView.as_view(),
        name='verify_email_complete'),
    path('check-verification-status/',
         check_verification_status,
         name='check_verification_status'),
]