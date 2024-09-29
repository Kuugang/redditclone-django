from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import models

# Utils
from main.utils import upload_image

def post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    return render(request, 'components/post/post_detail.html', {'post': post})

def submit(request):
    return render(request, 'submit.html')

def create_post(request):
    data = dict(request.POST.items())
    title = data.get("title")
    content = data.get("content")
    community = data.get("community")
    community = models.Community.objects.get(id=community)
    # TODO
    # flairs = data.get("flairs")

    post = models.Post(title = title, content = content, community = community, user = request.user)
    post.save()

    return redirect('community:community', community_name=community.name)

def upload_post_image(request):
    image = request.FILES.get("file")
    url = upload_image(image, "postImage")

    response_data = {
        'url' : url
    }

    return JsonResponse(response_data)

