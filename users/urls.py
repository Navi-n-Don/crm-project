from django.urls import path, include
from users import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('accounts/', include([
        path('personal-room/', include([
            path('', views.PersonView.as_view(), name='cabinet'),
            path('update/', views.PersonUpdate.as_view(), name='cabinet-update'),
            path('delete/', views.PersonDelete.as_view(), name='cabinet-delete'),
            path('change-password-set/', views.PersonPasswordChange.as_view(), name='change-password-set'),
        ])),
        path('password-reset/', include([
            path('', views.PersonPasswordReset.as_view(), name='password_reset'),
            path('done/', auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),
                 name='password_reset_done'),
            path('confirm/<uidb64>/<token>/',
                 auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),
                 name='password_reset_confirm'),
            path('complete/',
                 auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),
                 name='password_reset_complete'),
        ])),
    ])),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]