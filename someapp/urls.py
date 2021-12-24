from django.urls import path, include
from . import views

urlpatterns = [
    path('company-list/', include([
        path('', views.CompanyListView.as_view(), name='companies'),
        path('new-company/', views.CompanyCreate.as_view(), name='new-company'),
        path('<slug:slug>/', include([
            path('', views.CompanyDetailView.as_view(), name='company-details'),
            path('update/', views.CompanyUpdate.as_view(), name='update-company'),
            path('delete/', views.CompanyDelete.as_view(), name='delete-company'),
        ])),
        path('<slug:company_slug>/<slug:project_slug>/', include([
            path('', views.ProjectDetailView.as_view(), name='project-details'),
            path('new-project/', views.ProjectCreate.as_view(), name='new-project'),
            path('update/', views.ProjectUpdate.as_view(), name='update-project'),
            path('delete/', views.ProjectDelete.as_view(), name='delete-project'),
        ])),

    ])),
    path('project-list/', include([
        path('', views.ProjectListView.as_view(), name='projects'),
    ])),
]
