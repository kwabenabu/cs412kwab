"""django/mini_insta/mixins.py
contains reusable mixins for the mini_insta app."""
# file mixins.py
# author Kwabena Ampomah
# description Reusable mixins for the mini_insta app

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile


class AuthMixin(LoginRequiredMixin):
    """Reusable mixin to require login and fetch the logged-in Profile."""

    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

    def get_logged_in_profile(self):
        """Return a Profile for the current user; pick newest if multiple."""
        if not self.request.user.is_authenticated:
            return None
        return Profile.objects.filter(user=self.request.user).order_by('-pk').first()

