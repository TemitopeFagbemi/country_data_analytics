from datetime import datetime, timedelta
from airflow import DAG
from airflow.sdk import task
from include.pipeline.extract import api_connect
from include.pipeline.load_to_bucket import (
    load_to_bucket,
    upload_to_s3,
    clear_s3_files
)
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


default_args = {
    'owner': 'Country_Data',
    'start_date': datetime(2026, 3, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# -------------------------
# TASKS
# -------------------------

@task()
def extract_api_data():
    return api_connect()
   
@task()
def load_to_minio(data):
    load_to_bucket(data)

@task()
def clear_s3_stage():       
    clear_s3_files()  # delete files from bucket

@task()
def load_to_s3(data):
    upload_to_s3(data)

# -------------------------
# SNOWFLAKE TASKS
# -------------------------

create_raw = SQLExecuteQueryOperator(
    task_id="create_raw",
    conn_id="snowflake_conn",
    sql="""
        CREATE OR REPLACE TABLE COUNTRIES_DATA_RAW (
            data VARIANT
        );
    """
)

copy_into_snowflake =  SQLExecuteQueryOperator(
    task_id="copy_into_snowflake",
    conn_id="snowflake_conn",
    sql="""
        USE DATABASE COUNTRY_DB;
        USE SCHEMA PUBLIC;
        USE WAREHOUSE COMPUTE_WH;

        COPY INTO COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW
        FROM @countries_stage
        FILE_FORMAT = (TYPE = JSON)
        PATTERN = '.*countries_.*\\.json'
        ON_ERROR = 'CONTINUE';
    """
)

create_silver =  SQLExecuteQueryOperator(
    task_id="create_silver",
    conn_id="snowflake_conn",
    sql="""
        CREATE OR REPLACE TABLE COUNTRY_DB.PUBLIC.COUNTRIES_SILVER AS
        SELECT
            data:name.common::STRING AS country_name,
            data:region::STRING AS region,
            data:population::NUMBER AS population,
            data:capital[0]::STRING AS capital_city,
            OBJECT_KEYS(data:currencies)[0]::STRING AS currency_code,
            data:currencies[
                OBJECT_KEYS(data:currencies)[0]
            ].name::STRING AS currency_name
        FROM COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW
        WHERE data IS NOT NULL;
    """
)

create_gold =  SQLExecuteQueryOperator(
    task_id="create_gold",
    conn_id="snowflake_conn",
    sql="""
        CREATE OR REPLACE TABLE COUNTRY_DB.PUBLIC.COUNTRIES_GOLD AS
        SELECT
            country_name,
            region,
            capital_city,
            currency_code,
            currency_name,
            population,
            CASE 
                WHEN population >= 50000000 THEN 'Large'
                WHEN population >= 10000000 THEN 'Medium'
                ELSE 'Small'
            END AS population_category
        FROM COUNTRY_DB.PUBLIC.COUNTRIES_SILVER;
    """
)

# -------------------------
# DAG
# -------------------------

with DAG(
    dag_id='country_data_pipeline',
    description='Country Data Pipeline',
    default_args=default_args,
    schedule='@hourly',
    catchup=False,
    tags=["countries", "minio", "s3", "snowflake"],
) as dag:

    data = extract_api_data()

    minio_task = load_to_minio(data)

    clear_stage = clear_s3_stage()

    s3_task = load_to_s3(data)
    

    # KEY DESIGN CHOICE
    data >> minio_task
    data >> [clear_stage, s3_task]   # run in parallel

    # Snowflake depends ONLY on S3
    s3_task >> create_raw >> copy_into_snowflake >> create_silver >> create_gold