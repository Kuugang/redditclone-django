from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('<str:community_name>/', views.community, name='community'),
    path('create_community/', views.create_community, name='create_community'),
    path('edit_community_appearance/', views.edit_community_appearance, name = 'edit_community_appearance'),
    path('create_community_rule/', views.create_community_rule, name='create_community_rule'),
    path('edit_community_rule/', views.edit_community_rule, name='edit_community_rule'),
    path('edit_community_details/', views.edit_community_details, name='edit_community_details'),
    path('delete_community_rule/', views.delete_community_rule, name='delete_community_rule'),
    path('edit_community_topics/', views.edit_community_topics, name='edit_community_topics'),
    path('check_community_name_availability/', views.check_community_name_availability, name='check_community_name_availability'),
]