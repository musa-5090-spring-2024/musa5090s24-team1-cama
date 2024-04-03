from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent


@functions_framework.http
def extract_phl_opa_assessments(request):
    print('Extracting OPA Assessments data...')

    # Download the OPA Properties data as a CSV
    url = 'https://opendata-downloads.s3.amazonaws.com/assessments.csv'
    filename = DIRNAME / 'phl_opa_assessments.csv'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('INPUT_DATA_LAKE_BUCKET')
    blobname = 'raw/phl_opa_assessments/phl_opa_assessments.csv'

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {BUCKET_NAME}')

    return f'Downloaded to {filename} and uploaded to gs://{BUCKET_NAME}/{blobname}'
