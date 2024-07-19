import secret
import boto3
from botocore.exceptions import ClientError


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=secret.aws_access_key_id,
            aws_secret_access_key=secret.aws_secret_access_key,
            region_name=secret.aws_region,
            endpoint_url=secret.endpoint_url,
        )
        self.bucket_name = secret.bucket_name

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