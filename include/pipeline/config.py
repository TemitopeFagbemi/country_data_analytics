# This file contains the configuration for the pipeline, including API endpoints, MinIO credentials, and Snowflake credentials
import os
from dotenv import load_dotenv
import boto3
load_dotenv()

urls = {
  'url_1': 'https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages',
  'url_2': 'https://restcountries.com/v3.1/all?fields=area,population,continents'
}


# MinIO endpoints
url_endpoint = os.getenv('MINIO_ENDPOINT', 'http://host.docker.internal:9000')
access_key = os.getenv('MINIO_ROOT_USER')
secret_key = os.getenv('MINIO_ROOT_PASSWORD')


snowflake_user = os.getenv('SNOW_USER')
snowflake_password = os.getenv('SNOW_PASSWORD')
snowflake_account = os.getenv('SNOW_ACCOUNT')


client = boto3.client(
      's3',
      endpoint_url=url_endpoint, # MinIO endpoint
      aws_access_key_id=access_key, # Minio access key
      aws_secret_access_key=secret_key, # Minio secret key
      config=boto3.session.Config(signature_version='s3v4'),
      verify=False # Set to False if using HTTP
    )