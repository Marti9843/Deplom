from django.conf import settings
from .models import User

def email_verification(request):
    """Додає інформацію про верифікацію email до контексту шаблонів"""
    context = {}
    if request.user.is_authenticated:
        context['email_verified'] = request.user.email_verified
        context['email_verification_pending'] = not request.user.email_verified
    return context