from .models import Company, Phone, Email, Project, Cabinet
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, FormView


class CompanyListView(ListView):
    model = Company
    template_name = "someapp/companies.html"
    context_object_name = "companies"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones'] = Phone.objects.all()
        context['emails'] = Email.objects.all()
        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = "someapp/company-details.html"
    context_object_name = "company"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones'] = Phone.objects.all()
        context['emails'] = Email.objects.all()
        return context


class ProjectListView(ListView):
    model = Project
    template_name = "someapp/projects.html"
    context_object_name = "projects"
    paginate_by = 2


class ProjectDetailView(DetailView):
    model = Project
    template_name = "someapp/project-details.html"
    context_object_name = "project"


class CabinetListView(ListView):
    model = Cabinet
    template_name = "cabinet.html"
    context_object_name = "cabinet"