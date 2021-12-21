from django.urls import path, include
from . import views

urlpatterns = [
    path('company-list/', include([
        path('', views.CompanyListView.as_view(), name='companies'),
        path('<str:slug>/', views.CompanyDetailView.as_view(), name='company-details'),
        ])),
    path('project-list/', include([
        path('', views.ProjectListView.as_view(), name='projects'),
        path('<str:slug>/', views.ProjectDetailView.as_view(), name='project-details'),
        ])),
]