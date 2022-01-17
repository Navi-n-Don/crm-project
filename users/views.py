from typing import Any, Union, Optional
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from main import settings
from users.forms import PersonUpdateForm, PersonCreationForm
from users.models import Person
from django.views.generic import ListView, UpdateView, DeleteView, CreateView


class SignUp(CreateView):
    """Controller for registration a custom user"""
    form_class = PersonCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    email_subject = 'Welcome!'
    email_content_to_send = 'users/signup_email.html'
    messages_type = messages.SUCCESS

    def form_valid(self, form: PersonCreationForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
        if self.request.POST:
            form = PersonCreationForm(self.request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                signup_user = Person.objects.get(username=username)
                user_group = Group.objects.get(name='Users')
                user_group.user_set.add(signup_user)
                text_mail = render_to_string(
                    self.email_content_to_send,
                    {
                        'user_name': username,
                        'link': f"{self.request.scheme}://{self.request.get_host()}{self.success_url}",
                    }
                )
                send_mail(
                    self.email_subject,
                    None,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data.get('email')],
                    fail_silently=False,
                    html_message=text_mail,
                )
                messages.add_message(
                    self.request,
                    self.messages_type,
                    f'User {username} registered successfully',
                )
            else:
                return super().form_invalid(form)
        else:
            form = PersonCreationForm()
        return super().form_valid(form)


class LoginView(View):
    """Controller for log in"""
    template_name = 'users/login.html'
    messages_type_agree = messages.SUCCESS
    messages_type_disagree = messages.ERROR

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Method for getting the form data"""
        form = AuthenticationForm(data=request.POST)
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Union[HttpResponsePermanentRedirect,
                                                                             HttpResponseRedirect, HttpResponse]:
        """Method for processing the form data"""
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    self.request,
                    self.messages_type_agree,
                    f'Welcome, {username}!',
                )
                return redirect('companies')
            else:
                messages.add_message(
                    self.request,
                    self.messages_type_disagree,
                    f'Unfortunately, the user with username {username} is not registered on this website',
                )
                return redirect('login')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    """Controller for log out"""
    def get(self, request: HttpRequest) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
        """Method for getting the form data"""
        logout(request)
        return redirect(settings.LOGIN_URL)


class PersonView(LoginRequiredMixin, ListView):
    """Controller for viewing personal information for active person"""
    model = Person
    template_name = "users/cabinet.html"
    context_object_name = "selfroom"

    def get_queryset(self) -> Any:
        """Method for getting a queryset"""
        queryset = self.request.user
        return queryset


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    """Controller for update a personal data"""
    model = Person
    form_class = PersonUpdateForm
    permission_required = 'users.change_person'
    template_name_suffix = '_update'
    success_url = reverse_lazy('cabinet')
    messages_type = messages.SUCCESS
    email_content_to_send = 'users/cabinet_update_email.html'

    def get_object(self, queryset: Optional[Any] = None) -> Any:
        """Method for getting a object"""
        queryset = self.request.user
        return queryset

    def form_valid(self, form: PersonUpdateForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
        changed_poles = dict()
        for items in Person.objects.filter(username=self.request.user).values():
            for key, val in items.items():
                if val != form.cleaned_data.get(key) and form.cleaned_data.get(key) is not None:
                    changed_poles[key] = form.cleaned_data.get(key)

        text_mail = render_to_string(
            self.email_content_to_send,
            {
                'user_name': Person.objects.get(username=self.request.user),
                'updated': changed_poles,
                'link': f"{self.request.scheme}://{self.request.get_host()}{self.success_url}",
            }
        )
        send_mail(
            'Data Update',
            None,
            settings.EMAIL_HOST_USER,
            [form.cleaned_data.get('email')],
            fail_silently=False,
            html_message=text_mail,
        )
        messages.add_message(
            self.request,
            self.messages_type,
            f'Data has been changed successfully',
        )
        return super().form_valid(form)


class PersonDelete(PermissionRequiredMixin, DeleteView):
    """Controller for delete person"""
    model = Person
    permission_required = 'users.delete_person'
    success_url = reverse_lazy('login')

    def get_object(self, queryset: Optional[Any] = None) -> Any:
        """Method for getting a object"""
        queryset = self.request.user
        return queryset


class PersonPasswordChange(LoginRequiredMixin, PasswordChangeView):
    """Controller for update a user password"""
    template_name = 'users/person_password_change.html'
    success_url = reverse_lazy('cabinet')
    messages_type = messages.SUCCESS

    def form_valid(self, form: PasswordChangeForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
        send_mail(
            'Changed Password',
            'Your password has been changed successfully',
            settings.EMAIL_HOST_USER,
            [self.request.user.email],
            fail_silently=False,
        )
        messages.add_message(
            self.request,
            self.messages_type,
            f'Password has been changed successfully',
        )
        return super().form_valid(form)


class PersonPasswordReset(PasswordResetView):
    """Controller for reset a user password"""
    template_name = 'reset/password_reset_form.html'
    email_template_name = 'reset/password_reset_email.html'
    messages_type = messages.SUCCESS

    def form_valid(self, form: PasswordResetForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
        messages.add_message(
            self.request,
            self.messages_type,
            f"https://{form.cleaned_data.get('email').split('@')[-1]}",
        )
        return super().form_valid(form)
