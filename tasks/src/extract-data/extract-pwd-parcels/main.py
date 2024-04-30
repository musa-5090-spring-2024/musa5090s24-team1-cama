from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
import requests
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def extract_phl_pwd_parcels(request):
    print('Extracting PWD Parcels data...')

    # Download the PWD Parcels data as GeoJSON
    url = 'https://opendata.arcgis.com/datasets/84baed491de44f539889f2af178ad85c_0.geojson'
    filename = DIRNAME / 'phl_pwd_parcels.geojson'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded {filename}')

    # Upload the downloaded file to cloud storage
    BUCKET_NAME = os.getenv('INPUT_DATA_LAKE_BUCKET')
    blobname = 'raw/phl_pwd_parcels/phl_pwd_parcels.geojson'

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f'Uploaded {blobname} to {BUCKET_NAME}')

    return f'Downloaded to {filename} and uploaded to gs://{BUCKET_NAME}/{blobname}'
