from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('logout/', views.handle_logout, name='logout'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('create_community/', views.create_community, name='create_community'),
    path('r/<str:community_name>/', views.community, name='community'),
    path('submit/', views.submit, name='submit'),
    path('upload_post_image/', views.upload_post_image, name='upload_post_image'),
    path('create_post/', views.create_post, name='create_post'),
]