import boto3
import os
from config.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


# Function to create and authenticate the boto3 S3 client using constants from constants.py
def get_s3_client():
    # Check if the required environment variables are loaded
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_REGION:
        raise ValueError("Missing AWS credentials in the constants.py file")

    return boto3.client('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_REGION)


# Function to upload folder to S3
def upload_folder_to_s3(folder_path, bucket_name, s3_prefix=""):
    s3 = get_s3_client()  # Get the authenticated S3 client

    for root, _, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.join(s3_prefix, os.path.relpath(local_path, folder_path))
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded {file} to s3://{bucket_name}/{s3_key}")
