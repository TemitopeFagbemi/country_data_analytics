from pipeline.extract import api_connect
from pipeline.load_to_bucket import load_to_bucket
#from pipeline.load_to_snowflake import load_json_data_to_snowflake

def main():
    # Step 1: Extract data from source
    api_response = api_connect()

    # Step 2: Load data to bucket
    load_to_bucket(api_response)

    # # Step 3: Load data to Snowflake
    # load_to_snowflake(
    #  bucket = "your-bucket-name",
    #  file_key = "",
    #  target_table = "your_target_table",
    # )
    return None

main()