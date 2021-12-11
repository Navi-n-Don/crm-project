from django.urls import path
from . import views

urlpatterns = [
    path('company_list/', views.CompanyListView.as_view(), name='fulllist'),
    path('company_list/<str:slug>/', views.CompanyDetailView.as_view(), name='company-details'),
]