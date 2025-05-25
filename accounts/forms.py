from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Profile

User = get_user_model()

# Кастомні валідатори
class UkrainianPhoneValidator(RegexValidator):
    regex = r'^\+380\d{9}$'
    message = "Номер телефону повинен бути у форматі: '+380XXXXXXXXX' (12 цифр, Україна)"

class NameValidator(RegexValidator):
    regex = r'^[А-Яа-яЇїІіЄєҐґ\'\-]+$'
    message = "Може містити лише українські літери, дефіс та апостроф"

class UsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9_]+$'
    message = "Логін може містити лише латинські літери, цифри та _"

class PasswordValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9_!@#$%^&*]+$'
    message = "Пароль може містити лише латинські літери, цифри та _!@#$%^&*"

class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть вашу електронну пошту'
        }),
        required=True
    )

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть ваше ім'я"
        }),
        max_length=30,
        required=True,
        validators=[NameValidator()]
    )
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть ваше прізвище"
        }),
        max_length=30,
        required=True,
        validators=[NameValidator()]
    )
    phone = forms.CharField(
        label='Номер телефону',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380991234567'
        }),
        max_length=17,
        required=True,
        validators=[UkrainianPhoneValidator()]
    )
    email = forms.EmailField(
        label='Пошта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть вашу пошту'
        }),
        required=True
    )
    username = forms.CharField(
        label="Логін",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть логін"
        }),
        required=True,
        validators=[UsernameValidator()],
        help_text="Логін може містити лише латинські літери, цифри та _"
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        }),
        required=True,
        validators=[PasswordValidator()],
        help_text="Пароль може містити лише латинські літери, цифри та символи: _!@#$%%^&*"
    )
    password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Підтвердіть пароль'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Користувач з такою поштою вже існує')
        return email



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Користувач з таким логіном вже існує')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Відправляємо лист для підтвердження email
            if hasattr(self, 'request'):
                user.send_verification_email(request=self.request)
            else:
                user.send_verification_email()
        return user

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        validators=[NameValidator()]
    )
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        validators=[NameValidator()]
    )
    phone = forms.CharField(
        label='Номер телефону',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=17,
        required=True,
        validators=[UkrainianPhoneValidator()]
    )
    current_password = forms.CharField(
        label='Поточний пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password1 = forms.CharField(
        label='Новий пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        validators=[PasswordValidator()]
    )
    new_password2 = forms.CharField(
        label='Підтвердження пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label='Пошта',
            widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            initial=self.instance.email
        )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        current_password = cleaned_data.get('current_password')

        if new_password1 or new_password2:
            if not current_password:
                self.add_error('current_password', 'Для зміни пароля введіть поточний пароль')
            elif not self.instance.check_password(current_password):
                self.add_error('current_password', 'Невірний поточний пароль')
            elif new_password1 != new_password2:
                self.add_error('new_password2', 'Нові паролі не співпадають')
            elif len(new_password1) < 8:
                self.add_error('new_password1', 'Пароль повинен містити мінімум 8 символів')

        phone = cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            self.add_error('phone', 'Користувач з таким номером телефону вже існує')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user