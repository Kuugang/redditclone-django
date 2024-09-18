from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('logout/', views.handle_logout, name='logout'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('create_community/', views.create_community, name='create_community'),
    path('r/<str:community_name>/', views.community, name='community'),
]
