from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class EmailVerifiedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.email_verified

    def handle_no_permission(self):
        return redirect('accounts:verify_email')