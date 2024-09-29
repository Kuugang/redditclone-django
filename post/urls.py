from django.urls import path
from . import views

app_name = "post"

p_name = "post"
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('create_post/', views.create_post, name='create_post'),
    path('upload_post_image/', views.upload_post_image, name='upload_post_image'),
    path('<uuid:post_id>/', views.post, name='post'),
]