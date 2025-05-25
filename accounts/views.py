from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm, EmailVerificationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .decorators import email_verified_required
from django.core.exceptions import ValidationError


User = get_user_model()


def register_view(request):
    """Обробка реєстрації нового користувача"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Додаємо request до форми для відправки листа
            form.request = request
            user = form.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('accounts:verify_email_done')
                })
            return redirect('accounts:verify_email_done')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Обробка входу з перевіркою підтвердження email"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            if not user.email_verified:
                messages.error(request, 'Будь ласка, підтвердьте ваш email перед входом.')
                return redirect('accounts:verify_email')

            login(request, user)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/'
                })
            return redirect('home')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.get_json_data()
            })
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@email_verified_required
@login_required
def profile_view(request):
    """Перегляд та оновлення профілю"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль успішно оновлено!')

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('accounts:profile')

        # Обробка помилок для не-AJAX запитів
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label if field in form.fields else field
                        messages.error(request, f"{field_label}: {error}")
            return render(request, 'accounts/profile.html', {'form': form})

        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        })
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


def logout_view(request):
    """Вихід з системи"""
    logout(request)
    return redirect('home')


class VerifyEmailView(TemplateView):
    template_name = 'accounts/verify_email.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email_verified:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmailVerificationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.email_verified:
                    if user.send_verification_email(request):
                        messages.success(request, f"Лист підтвердження було відправлено на {email}")
                        return redirect('accounts:verify_email_done')
                    else:
                        messages.error(request, "Не вдалося відправити лист. Спробуйте пізніше.")
                else:
                    messages.info(request, 'Цей email вже підтверджено.')
                    return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, 'Користувача з таким email не знайдено.')

        return render(request, self.template_name, {'form': form})


class VerifyEmailDoneView(TemplateView):
    """Сторінка підтвердження відправки листа"""
    template_name = 'accounts/verify_email_done.html'


class VerifyEmailConfirmView(TemplateView):
    """Обробка посилання підтвердження email"""
    template_name = 'accounts/verify_email_confirm.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if (user.email_verification_token == token and
                    not user.email_verified and
                    not user.is_verification_token_expired()):
                user.email_verified = True
                user.email_verification_token = None
                user.email_verification_sent_at = None
                user.save()

                # Авторизуємо користувача
                login(request, user)

                # Оновлюємо сесію для синхронізації
                request.session.modified = True

                # Перенаправляємо з повідомленням
                messages.success(request, 'Ваш email успішно підтверджено!')
                return redirect('accounts:verify_email_complete')

            # Додаємо повідомлення про помилки
            if user.email_verified:
                messages.info(request, 'Цей email вже було підтверджено раніше.')
            elif user.is_verification_token_expired():
                messages.error(request, 'Термін дії посилання минув. Будь ласка, запросіть нове посилання.')

            return redirect('accounts:verify_email_complete')

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Посилання для підтвердження недійсне.')
            return render(request, self.template_name, {'valid': False})


class VerifyEmailCompleteView(LoginRequiredMixin, TemplateView):
    """Сторінка успішного підтвердження email"""
    template_name = 'accounts/verify_email_complete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.email_verified:
            return redirect('accounts:verify_email')
        return super().dispatch(request, *args, **kwargs)


def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.email_verified:
                user.send_verification_email(request)
                messages.success(request, 'Лист підтвердження було надіслано знову.')
            else:
                messages.info(request, 'Цей email вже підтверджено.')
        except User.DoesNotExist:
            messages.error(request, 'Користувача з таким email не знайдено.')

    return redirect('accounts:verify_email_done')

@login_required
def check_verification_status(request):
    """Перевіряє статус верифікації для AJAX запитів"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'verified': request.user.email_verified
        })
    return HttpResponseForbidden()
