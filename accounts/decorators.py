from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def email_verified_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.email_verified:
            return redirect('accounts:verify_email')
        return view_func(request, *args, **kwargs)
    return wrapper