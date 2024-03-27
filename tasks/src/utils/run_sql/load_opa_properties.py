from dotenv import load_dotenv
load_dotenv()

import os
from google.cloud import bigquery
import functions_framework

@functions_framework.http
def load_phl_opa_properties(request):
    print('Loading prepared OPA Properties data into BigQuery...')

    # Define your Cloud Storage bucket and blob name
    bucket_name = os.getenv('DATA_LAKE_BUCKET')
    blob_name = 'tables/phl_opa_properties/phl_opa_properties.jsonl'
    uri = f"gs://{bucket_name}/{blob_name}"

    # Define your BigQuery dataset and table name
    dataset_name = os.getenv('DATA_LAKE_DATASET')
    table_name = 'phl_opa_properties'

    # Initialize a BigQuery client
    bigquery_client = bigquery.Client()

    # Specify the job configuration for the load job
    # This example assumes the table schema is auto-detected
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True,
    )

    # Create the load job
    load_job = bigquery_client.load_table_from_uri(
        uri,
        f"{dataset_name}.{table_name}",
        job_config=job_config,
    )

    # Wait for the load job to complete
    load_job.result()

    print(f"Loaded data into '{dataset_name}.{table_name}' from {uri}")

    return f"Loaded data into '{dataset_name}.{table_name}' from {uri}", 200
