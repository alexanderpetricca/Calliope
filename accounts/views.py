from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser
from .forms import CustomUserChangeForm

from allauth.account.views import PasswordChangeView


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Overriding Allauth view to allow redirect.
    """

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
    
        return reverse_lazy('change_password_done')


class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'account/password_change_done.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class UpdateUserProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = 'accounts/updateprofile.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('view_profile')


    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        else:
            return False
