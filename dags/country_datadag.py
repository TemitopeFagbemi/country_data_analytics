# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.decorators import task
# from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
# from airflow.operators.bash import BashOperator
# import json
# import os


# # -------------------------
# # DEFAULTS
# # -------------------------
# default_args = {
#     'owner': 'Country_Data',
#     'start_date': datetime(2026, 3, 26),
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
# }

# # -------------------------
# # TASKS
# # -------------------------

# @task()
# def extract_api_data():
#     from include.pipeline.extract import api_connect
#     return api_connect()

# @task()
# def save_local_file(data):
#     file_path = "/tmp/countries.json"

#     with open(file_path, "w") as f:
#         for record in data:
#             f.write(json.dumps(record) + "\n")  # ✅ NDJSON

#     return file_path

# @task()
# def upload_to_s3(data):
#     import json
#     import boto3

#     s3 = boto3.client("s3")

#     s3.put_object(
#         Bucket="country-bucket2",
#         Key="bronze/countries.json",
#         Body=json.dumps(data)    # ✅ upload actual JSON, not file path
#     )
# # -------------------------
# # SNOWFLAKE TASKS
# # -------------------------

# create_raw = SQLExecuteQueryOperator(
#     task_id="create_raw",
#     conn_id="snowflake_conn",
#     sql="""
#         CREATE OR REPLACE TABLE COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW (
#             data VARIANT,
#             load_timestamp TIMESTAMP,
#             file_name STRING
#         );
#     """
# )

# copy_into_snowflake = SQLExecuteQueryOperator(
#     task_id="copy_into_snowflake",
#     conn_id="snowflake_conn",
#     sql="""
#         COPY INTO COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW (data, load_timestamp, file_name)
#         FROM (
#             SELECT
#                 $1,
#                 CURRENT_TIMESTAMP(),
#                 METADATA$FILENAME
#             FROM @COUNTRY_DB.PUBLIC.COUNTRIES_STAGE
#         )
#         FILE_FORMAT = (TYPE = JSON)
#         PATTERN = '.*countries.*\\.json';
#     """
# )

# # -------------------------
# # DAG
# # -------------------------

# with DAG(
#     dag_id='country_data_pipeline',
#     default_args=default_args,
#      start_date=datetime(2024, 1, 1),
#     schedule=None,
#     catchup=False,
#     tags=["countries", "snowflake", "dbt"],
# ) as dag:
    

#     dbt_run = BashOperator(
#     task_id="dbt_run",
#     bash_command="""
#     cd /usr/local/airflow/dbt/country_dbt_project &&
#     dbt run --profiles-dir /usr/local/airflow/dbt
#     """
# )

#     data = extract_api_data()

#     file_path = save_local_file(data)

#     upload = upload_to_s3(file_path)

#     # FLOW
#     data >> file_path >> upload
#     upload >> create_raw >> copy_into_snowflake >> dbt_run





from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.bash import BashOperator
import json
import os

# -------------------------
# DEFAULTS
# -------------------------
default_args = {
    'owner': 'Country_Data',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# -------------------------
# TASKS
# -------------------------

@task()
def extract_api_data():
    from include.pipeline.extract import api_connect
    return api_connect()


@task()
def save_local_file(data):
    file_path = "/tmp/countries.json"

    with open(file_path, "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")  # ✅ NDJSON format

    return file_path


@task()
def upload_to_s3(file_path):
    import boto3

    s3 = boto3.client("s3")

    with open(file_path, "rb") as f:
        s3.put_object(
            Bucket="country-bucket2",
            Key="bronze/countries.json",
            Body=f.read()   # ✅ correct: upload file content
        )

    return "uploaded"


# -------------------------
# SNOWFLAKE TASKS
# -------------------------

create_raw = SQLExecuteQueryOperator(
    task_id="create_raw",
    conn_id="snowflake_conn",
    sql="""
        CREATE OR REPLACE TABLE COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW (
            data VARIANT,
            load_timestamp TIMESTAMP,
            file_name STRING
        );
    """
)

copy_into_snowflake = SQLExecuteQueryOperator(
    task_id="copy_into_snowflake",
    conn_id="snowflake_conn",
    sql="""
        COPY INTO COUNTRY_DB.PUBLIC.COUNTRIES_DATA_RAW (data, load_timestamp, file_name)
        FROM (
            SELECT
                $1,
                CURRENT_TIMESTAMP(),
                METADATA$FILENAME
            FROM @COUNTRY_DB.PUBLIC.COUNTRIES_STAGE
        )
        FILE_FORMAT = (TYPE = JSON)
        PATTERN = '.*countries.*\\.json';
    """
)

# -------------------------
# DAG
# -------------------------

with DAG(
    dag_id='country_data_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=["countries", "snowflake", "dbt"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /usr/local/airflow/dbt/country_dbt_project &&
        dbt run --profiles-dir /usr/local/airflow/dbt
        """
    )

    # FLOW
    data = extract_api_data()
    file_path = save_local_file(data)
    upload = upload_to_s3(file_path)

    data >> file_path >> upload >> create_raw >> copy_into_snowflake >> dbt_run