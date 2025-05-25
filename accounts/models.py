from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


class User(AbstractUser):
    # Валідатор для українських номерів телефону
    phone_regex = RegexValidator(
        regex=r'^\+380\d{9}$',
        message="Номер телефону повинен бути у форматі: '+380XXXXXXXXX' (12 цифр, Україна)"
    )

    # Валідатор для імені та прізвища (літери, дефіс, апостроф)
    name_regex = RegexValidator(
        regex=r'^[А-Яа-яЇїІіЄєҐґ\'\-]+$',
        message="Може містити лише літери, дефіс та апостроф"
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Пошта',
        error_messages={
            'unique': 'Користувач з такою поштою вже існує.'
        }
    )

    first_name = models.CharField(
        max_length=30,
        verbose_name="Ім'я",
        validators=[name_regex],
        error_messages={
            'invalid': "Ім'я може містити лише літери, дефіс та апостроф"
        }
    )

    last_name = models.CharField(
        max_length=30,
        verbose_name="Прізвище",
        validators=[name_regex],
        error_messages={
            'invalid': "Прізвище може містити лише літери, дефіс та апостроф"
        }
    )

    phone = models.CharField(
        max_length=17,
        validators=[phone_regex],
        verbose_name='Номер телефону',
        unique=True,
        error_messages={
            'unique': 'Користувач з таким номером телефону вже існує.',
            'invalid': 'Номер телефону повинен бути у форматі: +380XXXXXXXXX'
        }
    )

    # Додаткові поля для підтвердження email
    email_verified = models.BooleanField(default=False, verbose_name='Email підтверджено')
    email_verification_token = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        verbose_name='Токен підтвердження email'
    )
    email_verification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Час відправки підтвердження'
    )

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.username})'

    def clean(self):
        super().clean()
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'Користувач з такою поштою вже існує.'})
        if User.objects.filter(phone=self.phone).exclude(pk=self.pk).exists():
            raise ValidationError({'phone': 'Користувач з таким номером телефону вже існує.'})

    def generate_verification_token(self):
        """Генерує унікальний токен для підтвердження email"""
        token = get_random_string(length=64)
        self.email_verification_token = token
        self.email_verification_sent_at = timezone.now()
        self.save()
        logger.info(f"Згенеровано новий токен для користувача {self.email}")
        return token

    def is_verification_token_expired(self):
        """Перевіряє чи токен протух"""
        if not self.email_verification_sent_at:
            return True
        expiration_hours = getattr(settings, 'EMAIL_VERIFICATION_EXPIRE_HOURS', 24)
        return (timezone.now() - self.email_verification_sent_at).total_seconds() > expiration_hours * 3600

    def send_verification_email(self, request=None):
        """Надсилає лист з посиланням для підтвердження email"""
        # Перевіряємо кеш для запобігання повторним відправкам
        cache_key = f'email_verification_sent_{self.pk}'
        if cache.get(cache_key):
            logger.warning(f"Спроба повторної відправки листа для {self.email}")
            return False

        # Генеруємо новий токен, якщо потрібно
        if not self.email_verification_token or self.is_verification_token_expired():
            self.generate_verification_token()

        # Будуємо URL для підтвердження
        if request:
            verification_url = request.build_absolute_uri(
                reverse('accounts:verify_email_confirm', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
                    'token': self.email_verification_token
                })
            )
        else:
            domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
            protocol = 'https' if not settings.DEBUG else 'http'
            verification_url = f"""{protocol}://{domain}{reverse('accounts:verify_email_confirm', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(self.pk)),
                'token': self.email_verification_token
            })}"""

        # Генеруємо та відправляємо лист
        subject = 'Підтвердження email для Sport Center'
        context = {
            'user': self,
            'verification_url': verification_url,
            'expiration_hours': getattr(settings, 'EMAIL_VERIFICATION_EXPIRE_HOURS', 24)
        }

        try:
            html_message = render_to_string('accounts/email_verification_email.html', context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [self.email],
                html_message=html_message,
                fail_silently=False
            )

            # Встановлюємо кеш на 5 хвилин
            cache.set(cache_key, True, 300)
            logger.info(f"Лист підтвердження успішно відправлено на {self.email}")
            return True
        except Exception as e:
            logger.error(f"Помилка відправки email для {self.email}: {str(e)}")
            return False


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Користувач'
    )

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f'Профіль {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Створення профілю при створенні нового користувача"""
    if created:
        Profile.objects.create(user=instance)
        # Відправка листа тепер відбувається у формі реєстрації


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Збереження профілю при оновленні користувача"""
    if hasattr(instance, 'profile'):
        instance.profile.save()