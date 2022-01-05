from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from interactions.forms import ActionForm, ActionUpdateForm
from interactions.models import Interaction, Star
from someapp.models import Project


class ActionDetailView(LoginRequiredMixin, DetailView):
    model = Interaction
    template_name = "interactions/interaction-details.html"
    context_object_name = "current"


class ActionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Interaction
    form_class = ActionForm
    permission_required = 'interactions.add_interaction'
    template_name = "interactions/new-action.html"

    def form_valid(self, form):
        action = form.save(commit=False)
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        action.project = project
        action.manager = self.request.user
        action.rating = get_object_or_404(Star, pk=1)
        with transaction.atomic():
            action.save()
        return redirect(reverse_lazy('project-details',
                                     kwargs={'company_slug': project.company.slug, "project_slug": project.slug}))


class ActionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Interaction
    form_class = ActionUpdateForm
    permission_required = 'interactions.change_interaction'
    template_name_suffix = '_update'


class ActionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Interaction
    permission_required = 'interactions.delete_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details',
                            kwargs={'company_slug': self.kwargs['company_slug'],
                                    "project_slug": self.kwargs['project_slug']})
