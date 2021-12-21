from django.urls import path, include
from . import views
from .models import Company

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('personal_room/', views.PersonView.as_view(), name='cabinet'),
    path('company-list/', include([
        path('', views.CompanyListView.as_view(), name='companies'),
        path('new-company/', views.CompanyCreate.as_view(), name='new-company'),
        path('<slug:slug>/', views.CompanyDetailView.as_view(), name='company-details'),
        path('<slug:slug>/new-project/', views.ProjectCreate.as_view(), name='new-project'),
        ])),
    path('project-list/', include([
        path('', views.ProjectListView.as_view(), name='projects'),
        path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project-details'),
        ])),
]