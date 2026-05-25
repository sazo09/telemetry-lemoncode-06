import boto3
from botocore.exceptions import ClientError

from config import get_creds


class S3Service:
    def __init__(self, region_name='eu-west-3'):
        """Init S3 client and resource"""
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=get_creds()["aws_key"],
                                      aws_secret_access_key=get_creds()[
                                          "aws_secret"],
                                      )
        self.region = region_name
        
    def create_bucket(self, bucket_name):
        """Create an S3 bucket"""
        try:
            self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
            print(f"Bucket '{bucket_name}' created successfully")
            return True
        except ClientError as e:
            print(f"Error creating bucket: {e}")
            return False
        
    def upload_file(self, file_path, bucket_name, object_key):
        """Upload a file to S3"""
        try:
             self.s3_client.upload_file(file_path, bucket_name, object_key)
             print(f"File '{file_path}' uploaded to '{bucket_name}/{object_key}'")
             return True
        except ClientError as e:
             print(f"Error uploading file: {e}")
             return False