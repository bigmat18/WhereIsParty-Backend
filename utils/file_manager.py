import os, boto3
from tempfile import SpooledTemporaryFile
from botocore.client import BaseClient
from typing import Union

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', default='AKIA2CTNZ3PLCPDWI37X')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', default='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')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME', default='gluteatfree-media-bucket')
AWS_BUCKET_URL = f"https://{AWS_S3_BUCKET_NAME}.s3.eu-south-1.amazonaws.com"


def s3() -> BaseClient:
    client = boto3.client(service_name='s3',
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY,
                          region_name='eu-south-1')

    return client


def upload_file(file: SpooledTemporaryFile, filename:str, path:str = '') -> Union[str, None]:
    if not file: return None
    
    final_path = f"{path}{filename}"
    
    client = s3()
    client.upload_fileobj(file, AWS_S3_BUCKET_NAME, final_path)
        
    return f"{AWS_BUCKET_URL}/{final_path}" 


def delete_file(path: str) -> bool:
    if not path: return False

    s3 = boto3.resource('s3')
    s3.Object(AWS_S3_BUCKET_NAME, path).delete()
    
    return True
    