from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
import logging

def load_to_snowflake():
    logging.info("Starting Snowflake load")

    hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")

    # sql = """
    # COPY INTO COUNTRIES_DATA_RAW
    # FROM @countries_stage
    # FILE_FORMAT = tsv_format;
    # """

    sql = """
    COPY INTO COUNTRIES_DATA_RAW (data, load_timestamp, file_name)
    FROM (
        SELECT
            $1,
            CURRENT_TIMESTAMP(),
            METADATA$FILENAME
        FROM @countries_stage
    )
    FILE_FORMAT = (TYPE = JSON)
    PATTERN = '.*countries_.*\\.json'
    ON_ERROR = 'CONTINUE'
    FORCE = FALSE;
    """

    hook.run(sql)

    logging.info("✅ Snowflake load complete")