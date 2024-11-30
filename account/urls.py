from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

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
    path('profile/settings/', login_required(views.profile_settings), name='profile_settings'),
    path('profile/settings/edit_display_name/', login_required(views.edit_display_name), name='edit_display_name'),
    path('profile/settings/edit_about/', login_required(views.edit_about), name='edit_about'),
    path('profile/settings/edit_avatar/', login_required(views.edit_avatar), name='edit_avatar'),
    path('profile/settings/edit_banner/', login_required(views.edit_banner), name='edit_banner'),
    path("profile/<str:username>", views.user_profile, name="user_profile"),
    path("follow/<str:user>", login_required(views.follow), name="follow"),
    path("unfollow/<str:user>", login_required(views.unfollow), name="unfollow"),
    path("search/", views.search, name="search"),

    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='components/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='components/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    # Test view
    path('raise-500/', views.raise_500, name='raise_500'),
]