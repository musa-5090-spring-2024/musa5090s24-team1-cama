from dotenv import load_dotenv
load_dotenv()

import os
import pathlib

from google.cloud import bigquery
import functions_framework


DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def load_opa_properties(request):
    print('Loading OPA Properties data...')

    # Initialize BigQuery client
    client = bigquery.Client()

# Environment and configuration setup
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    dataset_name = 'source'  # Dataset for external tables
    internal_dataset_name = 'core'  # Dataset for internal tables
    table_name = 'opa_properties'
    external_table_uri = f'gs://musa5090s24_team1_prepared_data/tables/phl_opa_properties/phl_opa_properties.jsonl'

    print(external_table_uri)

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the external table's schema
    # Adjust according to your JSONL structure
    schema = [
        bigquery.SchemaField("parcel_number", "STRING"),
        bigquery.SchemaField("owner_name", "STRING"),
        bigquery.SchemaField("property_address", "STRING"),
        # Add more fields here based on your JSONL file structure
    ]

    # Define external table configuration
    external_config = bigquery.ExternalConfig("NEWLINE_DELIMITED_JSON")
    external_config.source_uris = [external_table_uri]
    print(external_config.source_uris)
    external_config.schema = schema
    external_config.autodetect = True

    # Set the table ID for the external table
    external_table_id = f"{project_id}.{dataset_name}.{table_name}"
    print(external_table_id)
    table = bigquery.Table(external_table_id, schema=schema)
    table.external_data_configuration = external_config

    # Attempt to create or update the external table
    table = client.create_table(table, exists_ok=True)
    print(f"External table {external_table_id} created or updated successfully.")

    # Define SQL query for creating or updating an internal table in the 'core' dataset
    internal_table_id = f"{project_id}.{internal_dataset_name}.{table_name}"
    print(internal_table_id)
    sql = f"""
    CREATE OR REPLACE TABLE `{internal_table_id}` AS
    SELECT *, parcel_number AS property_id
    FROM `{external_table_id}`
    """

    # Execute the query to create or update the internal table
    query_job = client.query(sql)
    query_job.result()  # Wait for the job to complete
    print(f"Internal table {internal_table_id} created or updated successfully.")

    return (f"External table {external_table_id} created and internal table {internal_table_id} "
            "created or updated successfully.")
