from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.views import View
from main import settings
from users.models import Person
from .filters import CompanyFilter, ProjectFilter
from .forms import PhoneInlineFormSet, EmailInlineFormSet, ProjectForm
from .models import Company, Phone, Email, Project
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView


class LoginView(View):
    template_name = 'login.html'

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


class CompanyListView(ListView):
    model = Company
    template_name = "someapp/companies.html"
    context_object_name = "companies"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones'] = Phone.objects.all()
        context['emails'] = Email.objects.all()
        context['filterset'] = CompanyFilter(self.request.GET, queryset=self.get_queryset()).filters['o']
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('sorting', 'title')
        return ordering if ordering in ('title', 'created_date', '-title', '-created_date',) else 'title'

    def get_queryset(self):
        query = self.model.objects.order_by(self.get_ordering())
        return query


class CompanyDetailView(DetailView):
    model = Company
    template_name = "someapp/company-details.html"
    context_object_name = "company"

    def get_context_data(self, *, object_list=None, **kwargs):
        datas = Company.objects.filter(slug=self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['phones'] = Phone.objects.all()
        context['emails'] = Email.objects.all()
        context['projects'] = Project.objects.filter(company_id=datas[0].pk)
        return context


class CompanyCreate(PermissionRequiredMixin, CreateView):
    model = Company
    fields = ('title', 'contact_person', 'description', 'address',)
    permission_required = 'someapp.add_company'
    template_name = "someapp/new-company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone'] = PhoneInlineFormSet(self.request.POST)
            context['email'] = EmailInlineFormSet(self.request.POST)
        else:
            context['phone'] = PhoneInlineFormSet()
            context['email'] = EmailInlineFormSet()
        return context

    def form_valid(self, form):
        """
        Checking the validity of the form data
        """
        context = self.get_context_data(form=form)
        formsets = [context['phone'], context['email']]
        count = 0
        for formset in formsets:
            if formset.is_valid():
                response = super().form_valid(form)
                contacts = formset.save(commit=False)
                for contact in contacts:
                    contact.user = self.request.user
                    contact.company = self.object
                    contact.save()
                count += 1
                if count == len(formsets):
                    return response
            else:
                return super().form_invalid(form)


class ProjectListView(ListView):
    model = Project
    template_name = "someapp/projects.html"
    context_object_name = "projects"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = ProjectFilter(self.request.GET, queryset=self.get_queryset()).filters['o']
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('sorting', 'title')
        return ordering if ordering in ('title', 'begin', '-title', '-begin', 'end', '-end',) else 'title'

    def get_queryset(self):
        query = self.model.objects.order_by(self.get_ordering())
        return query


class ProjectDetailView(DetailView):
    model = Project
    template_name = "someapp/project-details.html"
    context_object_name = "project"


class ProjectCreate(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    permission_required = 'someapp.add_project'
    template_name = "someapp/new-project.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(ProjectCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Project()
        kwargs['instance'].creator = self.request.user
        kwargs['instance'].company = Company.objects.filter(slug=self.kwargs.get('slug'))[0]
        return kwargs

    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['creator'].limit_choices_to = {'username': self.request.user}
        modelform.base_fields['company'].limit_choices_to = {'title': Company.objects.filter(slug=self.kwargs.get('slug'))[0]}
        return modelform


class PersonView(LoginRequiredMixin, ListView):
    model = Person
    template_name = "cabinet.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
