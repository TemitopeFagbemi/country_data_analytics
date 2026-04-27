from urllib import response
import boto3
import json
import logging
from airflow.sdk import Variable
from datetime import datetime
from botocore.client import Config

logging.basicConfig(level=logging.INFO)


# ✅ MinIO upload (bronze layer)
def load_to_bucket(data):
    logging.info("Starting load_to_bucket")

    bucket_name = Variable.get("MINIO_BUCKET")
    filename = f"countries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    s3 = boto3.client(
        "s3",
        endpoint_url=Variable.get("MINIO_ENDPOINT"),
        aws_access_key_id=Variable.get("MINIO_ROOT_USER"),
        aws_secret_access_key=Variable.get("MINIO_ROOT_PASSWORD"),
        config=Config(signature_version='s3v4')
    )

    # ✅ Ensure bucket exists FIRST
    existing = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]

    if bucket_name not in existing:
        logging.info(f"Creating MinIO bucket: {bucket_name}")
        s3.create_bucket(Bucket=bucket_name)

    # ✅ Convert to newline-delimited JSON (Snowflake-friendly)
    body = "\n".join(json.dumps(record) for record in data)

    # ✅ Upload ONCE
    s3.put_object(
        Bucket=bucket_name,
        Key=f"bronze/{filename}",
        Body=body,
        ##ContentType="application/json"
    )

    logging.info(f"✅ Uploaded to MinIO: {filename}")

def clear_s3_files():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Variable.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=Variable.get("AWS_SECRET_ACCESS_KEY"),
        region_name=Variable.get("AWS_REGION")
    )
    
    bucket = Variable.get("S3_BUCKET")
    prefix = "bronze/"   # Ensure we target the correct folder in S3

    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if "Contents" in response:
        for obj in response["Contents"]:
            s3.delete_object(Bucket=bucket, Key=obj["Key"])
    
    logging.info("✅ S3 stage cleared")


# ✅ S3 upload (for Snowflake)
def upload_to_s3(data):
    logging.info("Uploading to AWS S3")
    
    filename = f"countries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"


    s3 = boto3.client(
        "s3",
        aws_access_key_id=Variable.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=Variable.get("AWS_SECRET_ACCESS_KEY"),
        region_name=Variable.get("AWS_REGION")
    )

    # convert list of dicts to newline-delimited JSON for Snowflake
    body = "\n".join(json.dumps(record) for record in data)

    s3.put_object(
        Bucket=Variable.get("S3_BUCKET"),
        Key=f"bronze/{filename}",
        Body =body
        # Body=json.dumps(data),
    )

    logging.info(f"✅ Uploaded to S3: {filename}")