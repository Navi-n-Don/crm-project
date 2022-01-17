from typing import Any, Dict, Type, Optional
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from interactions.forms import LikeForm
from interactions.models import Interaction
from main.filters import CompanyFilter, ProjectFilter, Filter
from main.utils import single, total, filter_status
from .forms import PhoneInlineFormSet, EmailInlineFormSet, ProjectForm, ProjectUpdateForm, CompanyForm
from .models import Company, Project
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView


class CompanyListView(LoginRequiredMixin, ListView):
    """Controller for viewing list of all created companies"""
    model = Company
    template_name = "someapp/companies.html"
    context_object_name = "companies"
    paginate_by = 2

    def get_context_data(self, *, object_list: Any = None, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super().get_context_data(**kwargs)
        context['filterset'] = CompanyFilter(self.request.GET, queryset=self.get_queryset()).filters['o']
        return context

    def get_ordering(self) -> str:
        """Method for getting a value string of ordering"""
        ordering = self.request.GET.get('sorting', 'title')
        return ordering if ordering in ('title', 'created_date', '-title', '-created_date',) else 'title'

    def get_queryset(self) -> Any:
        """Method for getting a queryset"""
        query = self.model.objects.order_by(self.get_ordering())
        return query


class CompanyDetailView(LoginRequiredMixin, DetailView):
    """Controller for viewing detailed information about company"""
    model = Company
    template_name = "someapp/company-details.html"
    context_object_name = "company"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        projects = filter_status(self.request.GET.get('sorting'), Project.objects.filter(
            company_id=self.model.objects.get(slug=self.kwargs['slug'])))
        paginator = Paginator(projects, 2)
        context['page_obj'] = paginator.get_page(self.request.GET.get('page'))
        return context


class CompanyCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Controller for create a new company"""
    model = Company
    form_class = CompanyForm
    permission_required = 'someapp.add_company'
    template_name = "someapp/new-company.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super(CompanyCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone'] = PhoneInlineFormSet(self.request.POST)
            context['email'] = EmailInlineFormSet(self.request.POST)
        else:
            context['phone'] = PhoneInlineFormSet()
            context['email'] = EmailInlineFormSet()
        return context

    def form_valid(self, form: CompanyForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
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


class CompanyUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Controller for update the company"""
    model = Company
    form_class = CompanyForm
    permission_required = 'someapp.change_company'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super(CompanyUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['phone'] = PhoneInlineFormSet(self.request.POST, instance=self.object)
            context['email'] = EmailInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['phone'] = PhoneInlineFormSet(instance=self.object)
            context['email'] = EmailInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form: CompanyForm) -> HttpResponseRedirect:
        """Checking the validity of the form data"""
        # context = self.get_context_data()
        # phones = context['phone']
        # emails = context['email']
        # with transaction.atomic():
        #     form.instance.user = self.request.user
        #     self.object = form.save()
        #
        #     if phones.is_valid():
        #         phones.instance = self.object
        #         phones.save()
        #         print(phones.deleted_objects)
        #
        #     if emails.is_valid():
        #         emails.instance = self.object
        #         emails.save()
        #
        # return super(CompanyUpdate, self).form_valid(form)

        context = self.get_context_data()
        formsets = [context['phone'], context['email']]
        for formset in formsets:
            if formset.is_valid():
                contacts = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                for contact in contacts:
                    contact.user = self.request.user
                    contact.company = self.object
                    contact.save()
            else:
                return super().form_invalid(form)
        return super().form_valid(form)


class CompanyDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Controller for delete company"""
    model = Company
    permission_required = 'someapp.delete_company'
    success_url = reverse_lazy('companies')


class ProjectListView(LoginRequiredMixin, ListView):
    """Controller for viewing list of all created projects"""
    model = Project
    template_name = "someapp/projects.html"
    context_object_name = "projects"
    paginate_by = 2

    def get_context_data(self, *, object_list: Any = None, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super().get_context_data(**kwargs)
        context['filterset'] = ProjectFilter(self.request.GET, queryset=self.get_queryset()).filters['o']
        return context

    def get_ordering(self) -> str:
        """Method for getting a value string of ordering"""
        ordering = self.request.GET.get('sorting', 'title')
        return ordering if ordering in ('title', 'begin', '-title', '-begin', 'end', '-end',) else 'title'

    def get_queryset(self) -> Any:
        """Method for getting a queryset"""
        query = self.model.objects.order_by(self.get_ordering())
        return query


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Controller for viewing detailed information about project"""
    model = Project
    filterset_class = Filter
    template_name = "someapp/project-details.html"
    context_object_name = "project"

    def get_context_data(self, *, object_list=None, **kwargs: Any) -> Dict[str, Any]:
        """Method for adding extra context"""
        context = super().get_context_data(**kwargs)
        context['rate'] = LikeForm()
        context['likes'] = single(self.model.objects, self.kwargs['project_slug'], self.request.user)
        context['total'] = total(self.model.objects, self.kwargs['project_slug'])
        context['filterset'] = self.filterset_class(
            self.request.GET, queryset=Interaction.objects.filter(
                project_id=self.model.objects.get(slug=self.kwargs['project_slug']).pk))
        paginator = Paginator(context['filterset'].qs, 2)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        return context

    def get_object(self, queryset: Optional[Any] = None) -> Any:
        """Method for getting a object"""
        queryset = self.model.objects.get(slug=self.kwargs['project_slug'])
        return queryset


class ProjectCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Controller for create a new project"""
    model = Project
    form_class = ProjectForm
    permission_required = 'someapp.add_project'
    template_name = "someapp/new-project.html"

    def get_form_kwargs(self) -> Dict[str, dict]:
        """Method for passing certain data to the form"""
        kwargs = super(ProjectCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Project()
        kwargs['instance'].creator = self.request.user
        kwargs['instance'].company = Company.objects.get(slug=self.kwargs.get('slug'))
        return kwargs

    def get_form_class(self) -> Type[BaseModelForm]:
        """Method for getting form class to process"""
        modelform = super().get_form_class()
        modelform.base_fields['creator'].limit_choices_to = {'username': self.request.user}
        modelform.base_fields['company'].limit_choices_to = {
            'title': Company.objects.get(slug=self.kwargs.get('slug'))}
        return modelform


class ProjectUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Controller for update the project"""
    model = Project
    form_class = ProjectUpdateForm
    permission_required = 'someapp.change_company'
    template_name_suffix = '_update'

    def get_object(self, queryset: Optional[Any] = None) -> Any:
        """Method for getting a object"""
        queryset = self.model.objects.get(slug=self.kwargs['project_slug'])
        return queryset


class ProjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Controller for delete project"""
    model = Project
    permission_required = 'someapp.delete_project'
    success_url = reverse_lazy('projects')
