from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.views.generic.base import View
from interactions.forms import ActionForm, LikeForm, KeywordForm
from interactions.models import Interaction, Like, Keyword
from main.utils import total
from someapp.models import Project


class ActionDetailView(LoginRequiredMixin, DetailView):
    model = Interaction
    template_name = "interactions/interaction-details.html"
    context_object_name = "current"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = total(Project.objects, self.kwargs['project_slug'])
        return context


class ActionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Interaction
    form_class = ActionForm
    permission_required = 'interactions.add_interaction'
    template_name = "interactions/new-action.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = self.kwargs
        return context

    def form_valid(self, form):
        action = form.save(commit=False)
        project = get_object_or_404(Project, slug=self.kwargs['project_slug'])
        action.project = project
        action.manager = self.request.user
        with transaction.atomic():
            action.save()
            form.save_m2m()
        return redirect(reverse_lazy('project-details',
                                     kwargs={'company_slug': project.company.slug,
                                             "project_slug": project.slug}))


class ActionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Interaction
    form_class = ActionForm
    permission_required = 'interactions.change_interaction'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = self.kwargs
        return context

    def get_success_url(self):
        return reverse_lazy('project-details',
                            kwargs={'company_slug': self.kwargs['company_slug'],
                                    "project_slug": self.kwargs['project_slug']})


class ActionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Interaction
    permission_required = 'interactions.delete_interaction'

    def get_success_url(self):
        return reverse_lazy('project-details',
                            kwargs={'company_slug': self.kwargs['company_slug'],
                                    "project_slug": self.kwargs['project_slug']})


class AddLikeView(View):
    def post(self, request):
        form = LikeForm(request.POST)
        if form.is_valid():
            Like.objects.update_or_create(
                who_id=self.request.user.id,
                action_id=int(request.POST.get("post")),
                defaults={'like_id': int(request.POST.get("like"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class CreateKeyword(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Keyword
    form_class = KeywordForm
    permission_required = 'interactions.add_keyword'
    template_name = "interactions/new-keyword.html"

    def get_success_url(self):
        return reverse_lazy('new-action',
                            kwargs={'company_slug': self.kwargs['company_slug'],
                                    "project_slug": self.kwargs['project_slug']})


class FilterKeywordView(LoginRequiredMixin, ListView):
    model = Interaction
    template_name = "interactions/interactions.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = self.model.objects.filter(keyword__in=self.request.GET.getlist('keyword'))
        return queryset
