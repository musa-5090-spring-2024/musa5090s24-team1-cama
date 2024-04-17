from dotenv import load_dotenv
load_dotenv()

import os
import pathlib

from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import functions_framework


DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def load_opa_assessments(request):
    print('Loading OPA Assessments data...')

# Environment and configuration setup
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    dataset_name = 'source'  # Dataset for external tables
    internal_dataset_name = 'core'  # Dataset for internal tables
    table_name = 'opa_assessments'
    external_table_uri = f'gs://musa5090s24_team1_prepared_data/tables/phl_opa_assessments/phl_opa_assessments.jsonl'

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the external table's schema
    # Adjust according to your JSONL structure
    schema = [
        bigquery.SchemaField("parcel_number", "STRING"),
        bigquery.SchemaField("year", "STRING"),
        bigquery.SchemaField("market_value", "FLOAT"),
        bigquery.SchemaField("taxable_land", "FLOAT"),
        bigquery.SchemaField("taxable_building", "FLOAT"),
        bigquery.SchemaField("exempt_land", "FLOAT"),
        bigquery.SchemaField("exempt_building", "FLOAT"),
        bigquery.SchemaField("objectid", "STRING"),
        # Add more fields here based on your JSONL file structure
    ]

    # Define external table configuration
    external_config = bigquery.ExternalConfig("NEWLINE_DELIMITED_JSON")
    external_config.source_uris = [external_table_uri]
    print(external_config.source_uris)
    external_config.schema = schema
    external_config.autodetect = False

    # Set the table ID for the external table
    external_table_id = f"{project_id}.{dataset_name}.{table_name}"

    # Attempt to get the table to check if it exists
    try:
        existing_table = client.get_table(external_table_id)
        print(f"Table {existing_table.table_id} exists. Deleting...")
        client.delete_table(existing_table)
        print(f"Table {existing_table.table_id} deleted.")
    except NotFound:
        print(f"Table {external_table_id} not found. Will create a new one.")

    table = bigquery.Table(external_table_id, schema=schema)
    table.external_data_configuration = external_config
    
    # Create the external table
    try:
        table = client.create_table(table)
        print(f"External table {table.table_id} created successfully.")
    except Exception as e:
        print(f"Failed to create external table {table.table_id}. Error: {e}")
        return

    # Define SQL query for creating or updating an internal table in the 'core' dataset
    internal_table_id = f"{project_id}.{internal_dataset_name}.{table_name}"
    sql = f"""
    CREATE OR REPLACE TABLE `{internal_table_id}` AS
    SELECT *, parcel_number as property_id
    FROM `{external_table_id}`
    """
    
    # Execute the query to create or update the internal table
    try:
        query_job = client.query(sql)
        query_job.result()  # Wait for the job to complete
        print(f"External table {external_table_id} created and internal table {internal_table_id} created or updated successfully.")
        return f"External table {external_table_id} created and internal table {internal_table_id} created or updated successfully.", 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return error_message, 500
    
    # Make sure the function always has a return statement at the end
    return "An unexpected error occurred", 500