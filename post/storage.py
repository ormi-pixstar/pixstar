import boto3
from myapp.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME
import random

URL_FORMAT = "https://{bucketName}.s3.{region}.amazonaws.com/{imageName}"


class S3Storage():
    def __init__(self):
        self.region = AWS_REGION
        self.bucket = AWS_STORAGE_BUCKET_NAME
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name = self.region
        )

    def upload(self, post_pk, imageName):
        ran = random.uniform(0, 10)
        self.imageName = "{post_pk}_{random}_{imageName}".format(
            post_pk = post_pk,
            random = ran,
            imageName = imageName
        )

        self.s3_resource.Bucket(self.bucket).put_object(
            Key = self.imageName,
            Body = imageName
        )

    def getUrl(self):
        url = URL_FORMAT.format(
            region = self.region,
            bucketName = self.bucket,
            imageName = self.imageName
        )
        return url
    
    def delete(self, imageName):
        name = imageName.image_url.split('/')[-1]
        self.s3_resource.Object(self.bucket, name).delete()