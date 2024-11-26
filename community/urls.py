from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

app_name = 'community'

urlpatterns = [
    path('create_community/', views.create_community, name='create_community'),
    path('join_community/<str:community_name>', views.join_community, name='join_community'),
    path('leave_community/<str:community_name>', views.leave_community, name='leave_community'),
    path('invite/', views.invite_users_to_community, name='invite_users_to_community'),
    path('invite_users_lookup/', views.lookup_community_invite_eligible_users, name='lookup_community_invite_eligible_users'),
    path('invites/', views.community_invites, name='community_invites'),

    path('invite/accept/<uuid:invite_id>', views.accept_community_invite, name='accept_community_invite'),
    path('invite/reject/<uuid:invite_id>', views.reject_community_invite, name='reject_community_invite'),

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