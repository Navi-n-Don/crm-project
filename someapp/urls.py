from django.urls import path
from . import views

urlpatterns = [
    path('personal_room/', views.CabinetListView.as_view(), name='cabinet'),
    path('company_list/', views.CompanyListView.as_view(), name='companies'),
    path('company_list/<str:slug>/', views.CompanyDetailView.as_view(), name='company-details'),
    path('project_list/', views.ProjectListView.as_view(), name='projects'),
    path('project_list/<str:slug>/', views.ProjectDetailView.as_view(), name='project-details'),
]