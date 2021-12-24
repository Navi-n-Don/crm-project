from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from main import settings
from users.forms import PersonUpdateForm
from users.models import Person
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView


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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PersonUpdate(PermissionRequiredMixin, UpdateView):
    model = Person
    form_class = PersonUpdateForm
    permission_required = 'users.change_person'
    template_name_suffix = '_update'
    success_url = reverse_lazy('cabinet')

    def get_context_data(self, **kwargs):
        context = super(PersonUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        queryset = self.model.objects.filter(username=self.request.user).first()
        return queryset


class PersonDelete(PermissionRequiredMixin, DeleteView):
    model = Person
    permission_required = 'users.delete_person'
    success_url = reverse_lazy('cabinet')
