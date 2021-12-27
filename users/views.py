from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from interactions.models import Interaction
from main import settings
from users.forms import PersonUpdateForm, PersonCreationForm
from users.models import Person
from django.views.generic import ListView, UpdateView, DeleteView, CreateView


class SignUp(CreateView):
    form_class = PersonCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        if self.request.POST:
            form = PersonCreationForm(self.request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                signup_user = Person.objects.get(username=username)
                user_group = Group.objects.get(name='Users')
                user_group.user_set.add(signup_user)
            else:
                return super().form_invalid(form)
        else:
            form = PersonCreationForm()
        return super().form_valid(form)


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('companies')
            else:
                return redirect('login')

        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)


class PersonView(LoginRequiredMixin, ListView):
    model = Person
    template_name = "users/cabinet.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interaction'] = []
        for action in Interaction.objects.filter(manager_id=self.request.user.id):
            context['interaction'].append(action)
        return context


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    model = Person
    form_class = PersonUpdateForm
    permission_required = 'users.change_person'
    template_name_suffix = '_update'
    success_url = reverse_lazy('cabinet')

    def get_object(self, queryset=None):
        queryset = self.request.user
        return queryset


class PersonDelete(PermissionRequiredMixin, DeleteView):
    model = Person
    permission_required = 'users.delete_person'
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        queryset = self.request.user
        return queryset
