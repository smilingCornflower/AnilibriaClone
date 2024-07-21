from Anilibria import settings
import boto3
from botocore.exceptions import ClientError


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.ENDPOINT_URL,
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_fileobj(self, file_obj, object_name) -> bool:
        try:
            self.s3_client.upload_fileobj(Fileobj=file_obj,
                                          Bucket=self.bucket_name,
                                          Key=object_name
                                          )
            return True
        except ClientError as e:
            print(f"s3_service.py upload_fileobj: {e}")
            return False

    def get_url(self, object_name):
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=60  # 1 min
            )
            return url
        except ClientError as e:
            print(f"s3_service.py upload_file: {e}")
            return False

    def delete_file(self, object_name) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name,
                                         Key=object_name
                                         )
            return True
        except ClientError as e:
            print(f"s3_service.py delete_file: {e}")
            return False


s3 = S3Service()