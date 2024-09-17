import requests, os, uuid


def get_request_data(request, inputs, files):
    pass 

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

