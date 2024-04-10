from dotenv import load_dotenv
load_dotenv()

import os
import pathlib

from google.cloud import bigquery
import functions_framework


DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def load_pwd_parcels(request):
    print('Loading PWD Parcels data...')

    # Initialize BigQuery client
    client = bigquery.Client()

# Environment and configuration setup
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    dataset_name = 'source'  # Dataset for external tables
    internal_dataset_name = 'core'  # Dataset for internal tables
    table_name = 'pwd_parcels'
    external_table_uri = f'gs://musa5090s24_team1_prepared_data/tables/phl_pwd_parcels/phl_pwd_parcels.jsonl'

    print(external_table_uri)

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the external table's schema
    schema = [
        bigquery.SchemaField("OBJECTID", "STRING"),
        bigquery.SchemaField("PARCELID", "STRING"),
        bigquery.SchemaField("TENCODE", "STRING"),
        bigquery.SchemaField("ADDRESS", "STRING"),
        bigquery.SchemaField("OWNER1", "STRING"),
        bigquery.SchemaField("OWNER2", "STRING", mode="NULLABLE"),  # Assuming OWNER2 can be null
        bigquery.SchemaField("BLDG_DESC", "STRING"),
        bigquery.SchemaField("IMPERV_AREA", "INTEGER"),
        bigquery.SchemaField("BC_LANDUSE", "STRING"),
        bigquery.SchemaField("BC_TYPE", "STRING"),
        bigquery.SchemaField("IMP_ROOF", "FLOAT"),
        bigquery.SchemaField("IMP_GROUND", "FLOAT"),
        bigquery.SchemaField("IMP_TOTAL", "FLOAT"),
        bigquery.SchemaField("NATURAL_GROUND", "FLOAT"),
        bigquery.SchemaField("TOTAL_GROUND", "FLOAT"),
        bigquery.SchemaField("COUNCIL_DISTRICT", "STRING"),
        bigquery.SchemaField("PCPC_DISTRICT", "STRING"),
        bigquery.SchemaField("PUBLIC_PRIVATE", "STRING"),
        bigquery.SchemaField("PROGRAM", "STRING"),
        bigquery.SchemaField("OWNER_CATEGORY", "STRING"),
        bigquery.SchemaField("Shape__Area", "FLOAT"),
        bigquery.SchemaField("Shape__Length", "FLOAT"),
        bigquery.SchemaField("geometry", "GEOGRAPHY"),
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
    SELECT *
    FROM `{external_table_id}`
    """

    # Execute the query to create or update the internal table
    query_job = client.query(sql)
    query_job.result()  # Wait for the job to complete
    print(f"Internal table {internal_table_id} created or updated successfully.")

    return (f"External table {external_table_id} created and internal table {internal_table_id} "
            "created or updated successfully.")
