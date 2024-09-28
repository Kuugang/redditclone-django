from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('logout/', views.handle_logout, name='logout'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),

    # Community
    path('r/<str:community_name>/', views.community, name='community'),
    path('create_community/', views.create_community, name='create_community'),
    path('edit_community_appearance/', views.edit_community_appearance, name = 'edit_community_appearance'),
    path('create_community_rule/', views.create_community_rule, name='create_community_rule'),
    path('edit_community_rule/', views.edit_community_rule, name='edit_community_rule'),
    path('edit_community_details/', views.edit_community_details, name='edit_community_details'),
    path('delete_community_rule/', views.delete_community_rule, name='delete_community_rule'),
    path('edit_community_topics/', views.edit_community_topics, name='edit_community_topics'),
    path('check_community_name_availability/', views.check_community_name_availability, name='check_community_name_availability'),

    # Post
    path('submit/', views.submit, name='submit'),
    path('upload_post_image/', views.upload_post_image, name='upload_post_image'),
    path('create_post/', views.create_post, name='create_post'),
]
