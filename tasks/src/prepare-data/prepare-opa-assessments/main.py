import csv
import json
import os
import pathlib
from google.cloud import storage
import functions_framework

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def prepare_phl_opa_assessments(request):
    print('Preparing OPA Assessments data...')

    # Environment setup
    bucket_name = os.getenv('INPUT_DATA_LAKE_BUCKET')
    output_bucket_name = os.getenv('OUTPUT_DATA_LAKE_BUCKET')

    # File and blob setup
    raw_blobname = 'raw/phl_opa_assessments/phl_opa_assessments.csv'
    prepared_blobname = 'tables/phl_opa_assessments/phl_opa_assessments.jsonl'

    # Initialize Cloud Storage client
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)
    output_bucket = storage_client.bucket(output_bucket_name)

    # Download the raw csv file
    raw_blob = input_bucket.blob(raw_blobname)
    raw_filename = '/tmp/phl_opa_assessments.csv'
    raw_blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Convert CSV to JSONL
    jsonl_filename = '/tmp/phl_opa_assessments.jsonl'
    with open(raw_filename, 'r') as csv_file, open(jsonl_filename, 'w') as jsonl_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json.dump(row, jsonl_file)
            jsonl_file.write('\n')

    print(f'Converted CSV to JSONL: {jsonl_filename}')

    # Upload the prepared JSONL file to Cloud Storage
    prepared_blob = output_bucket.blob(prepared_blobname)
    prepared_blob.upload_from_filename(jsonl_filename)
    print(f'Uploaded JSONL to gs://{output_bucket_name}/{prepared_blobname}')

    return f'Converted CSV to JSONL: {jsonl_filename} and uploaded to gs://{output_bucket_name}/{prepared_blobname}', 200
