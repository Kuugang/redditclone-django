from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = "post"

urlpatterns = [
    path('submit/', login_required(views.submit), name='submit'),
    path('<str:community_name>/submit/', views.submit, name='submit_with_community'),
    path('create_post/', views.create_post, name='create_post'),
    path('upload_post_image/', views.upload_post_image, name='upload_post_image'),
    path('<uuid:post_id>/', views.post, name='post'),
    path('vote/<uuid:post_id>/<str:vote_type>', views.vote, name='vote'),
    path('comment/uuid:post_ud/<str:comment>',  views.comment, name='vote')
]