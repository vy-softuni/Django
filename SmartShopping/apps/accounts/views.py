from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import views as auth_views
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.accounts.forms import SignUpForm, ProfileForm


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'
    extra_context = {'title': "Sign Up"}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signin.html'
    extra_context = {'title': "Sign In"}


@method_decorator(login_required, name='dispatch')
class LogoutView(auth_views.LogoutView):
    extra_context = {'title': "Logout"}


@method_decorator(login_required, name='dispatch')
class ProfileView(UpdateView):
    template_name = "accounts/profile.html"
    form_class = ProfileForm
    model = get_user_model()
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user
