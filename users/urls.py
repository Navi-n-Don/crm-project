from django.urls import path, include
from users import views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('personal-room/', include([
        path('', views.PersonView.as_view(), name='cabinet'),
        path('update/', views.PersonUpdate.as_view(), name='cabinet-update'),
        path('delete/', views.PersonDelete.as_view(), name='cabinet-delete'),
    ])),
]