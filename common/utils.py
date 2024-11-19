import requests, os, uuid
from post.models import Comment


def get_request_data(request, inputs, files):
    pass 

def upload_local_image(image, folder: str):
    if image:
        upload_uid = str(uuid.uuid4())

        STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')
        extension = image.content_type
        extension = extension.split("/")[1]
        STATIC_PATH = f"images/{folder}/{upload_uid}.{extension}"
        image_path = f"{STATIC_ROOT}/{STATIC_PATH}"

        print(image_path)

        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        return STATIC_PATH

def upload_image(image, bucket: str):
    if image:
        api_key = os.getenv("SUPABASE_API_KEY")

        upload_uid = str(uuid.uuid4())

        bucket_URL = f"https://{os.getenv("SUPABASE_REFERENCE_ID")}.supabase.co/storage/v1/object/{bucket}/"
        public_bucket_URL = f"https://{os.getenv("SUPABASE_REFERENCE_ID")}.supabase.co/storage/v1/object/public/{bucket}/"
        image_URL = f"{bucket_URL}{upload_uid}{os.path.splitext(image._name)[1]}"

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': image.content_type
        }

        try:
            response = requests.post(image_URL, headers=headers, data=image.read())
            
            if response.status_code == 200:
                return image_URL
            else:
                print("Failed to upload image:", response.json())
                return None
        except Exception as e:
            print("An error occurred during image upload:", e)
            return None


    else:
        return None


def get_child_comments(comment, depth=0):
    comments = Comment.objects.filter(parent=comment.id)
    child_comments = []

    if comments:
        for child in comments:
            child_comment_data = {
                'comment' : child,
                'depth': depth,
                'children': get_child_comments(child, depth=depth+1), 
            }
            child_comments.append(child_comment_data)
    child_comments.reverse()
    return child_comments