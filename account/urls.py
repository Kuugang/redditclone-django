from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('check_availability/', views.check_availability, name='check_availability'),
    # path('logout/', views.handle_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('profile/', views.profile, name='profile'),
]