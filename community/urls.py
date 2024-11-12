from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

app_name = 'community'

urlpatterns = [
    path('create_community/', views.create_community, name='create_community'),
    path('join_community/<str:community_name>', views.join_community, name='join_community'),
    path('edit_community_appearance/', login_required(views.edit_community_appearance), name = 'edit_community_appearance'),
    path('create_community_rule/', login_required(views.create_community_rule), name='create_community_rule'),
    path('edit_community_rule/', login_required(views.edit_community_rule), name='edit_community_rule'),
    path('edit_community_details/',login_required(views.edit_community_details), name='edit_community_details'),
    path('delete_community_rule/', login_required(views.delete_community_rule), name='delete_community_rule'),
    path('edit_community_topics/', login_required(views.edit_community_topics), name='edit_community_topics'),
    path('check_community_name_availability/', views.check_community_name_availability, name='check_community_name_availability'),
    path('<str:community_name>/', views.community, name='community'),

    path('<str:community_name>/event', views.event , name='event'),
]