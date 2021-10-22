import boto3
import os

class S3:
    def __init__(self, bucket_name):
        s3 = boto3.resource('s3')
        self.bucket = s3.Bucket(bucket_name)

    def upload_image(self, file_name):
        self.bucket.put_object(Key=file_name, Body=open(os.path.join("pics", file_name), 'rb'))



