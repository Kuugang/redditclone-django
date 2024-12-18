from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = "post"

urlpatterns = [
    path('submit/', login_required(views.submit), name='submit'),
    path('<str:community_name>/submit/', views.submit, name='submit_with_community'),
    path('create_post/<str:community_name>/', views.create_post, name='create_post'),
    path('upload_post_image/', views.upload_post_image, name='upload_post_image'),
    path('<uuid:post_id>/', views.post, name='post'),

    # let url = `/post/vote/${contentId}/${voteType}`
    path('vote/<uuid:content_id>/<str:vote>/<str:type>/', views.vote, name='vote_post'),


    path('comment/<uuid:post_id>',  views.comment, name='comment'),
    path('comment/edit/<uuid:comment_id>',  views.edit_comment, name='edit_comment'),
    path('delete_comment/',  (views.delete_comment), name='delete_comment'),
    path('delete/',  login_required(views.delete_post), name='delete_post'),
    path('<uuid:post_id>/edit/',  login_required(views.edit_post), name='edit_post'),

    # Should probably make next 2 into 1 view
    path("save/", login_required(views.save_post), name="save_post"),
    path("unsave/", login_required(views.unsave_post), name="unsave_post"),
    path("report_post/", login_required(views.report_post), name="report_post"),
]