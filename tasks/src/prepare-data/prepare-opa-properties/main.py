from dotenv import load_dotenv
load_dotenv()

import json
import os
import pathlib

import logging
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform
import functions_framework
from google.cloud import storage

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def prepare_phl_opa_properties(request):
    print('Preparing OPA Properties data...')

    raw_filename = DIRNAME / 'opa_properties_public.geojson'
    prepared_filename = DIRNAME / 'phl_opa_properties.jsonl'

    # Download the data from the input bucket
    raw_blobname = 'raw/phl_opa_properties/phl_opa_properties.csv'
    prepared_blobname = 'tables/phl_opa_properties/phl_opa_properties.jsonl'
    
    bucket_name = os.getenv('INPUT_DATA_LAKE_BUCKET')
    output_bucket_name = os.getenv('OUTPUT_DATA_LAKE_BUCKET')
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)
    output_bucket = storage_client.bucket(output_bucket_name)

    blob = input_bucket.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set up the projection
    transformer = pyproj.Transformer.from_proj('epsg:2272', 'epsg:4326', always_xy=True)

    def process_data(geojson_data, prepared_filename):
        # Open the output file for writing
        with open(prepared_filename, 'w') as f:
            for feature in geojson_data['features']:
                geom = shape(feature['geometry'])
                # Apply transformation directly to the Shapely geometry
                transformed_geom = transform(transformer.transform, geom)
                feature['geometry'] = mapping(transformed_geom)
                # Write each transformed feature as a separate line in JSONL format
                f.write(json.dumps(feature) + '\n')

     logging.info(f'Processed data into {prepared_filename}')

    blob = output_bucket.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname} in {output_bucket_name}')

    return f'Processed data into {prepared_filename} and uploaded to gs://{output_bucket_name}/{prepared_blobname}'