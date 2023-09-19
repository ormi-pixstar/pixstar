import os
import boto3
from .utils import unique_filename


def upload_images_to_s3(images):
    image_urls = []
    for image in images:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        )
        file_name = unique_filename(image.name)
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        s3.upload_fileobj(
            image, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'}
        )
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        image_urls.append(image_url)
    return image_urls
