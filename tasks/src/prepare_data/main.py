from dotenv import load_dotenv
load_dotenv()

import csv
import json
import os
import pathlib

import pyproj
from shapely import wkt
import functions_framework
from google.cloud import storage
import pretty_errors

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def prepare_phl_opa_properties(request):
    print('Preparing OPA Properties data...')

    raw_filename = DIRNAME / 'phl_opa_properties.csv'
    prepared_filename = DIRNAME / 'phl_opa_properties.jsonl'

    # Input bucket
    bucket_name = os.getenv('INPUT_DATA_LAKE_BUCKET')
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)

    # Output bucket
    output_bucket_name = os.getenv('OUTPUT_DATA_LAKE_BUCKET')  # New environment variable for output bucket
    output_bucket = storage_client.bucket(output_bucket_name)

    # Download the data from the input bucket
    raw_blobname = 'raw/phl_opa_properties/phl_opa_properties.csv'
    blob = input_bucket.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the CSV file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    # Set up the projection
    transformer = pyproj.Transformer.from_proj('epsg:2272', 'epsg:4326')

    # Write the data to a JSONL file
    with open(prepared_filename, 'w') as f:
        for i, row in enumerate(data):
            geom_wkt = row.pop('shape').split(';')[1]
            if geom_wkt == 'POINT EMPTY':
                row['geog'] = None
            else:
                geom = wkt.loads(geom_wkt)
                x, y = transformer.transform(geom.x, geom.y)
                row['geog'] = f'POINT({x} {y})'
            f.write(json.dumps(row) + '\n')

    print(f'Processed data into {prepared_filename}')

    # Upload the prepared data to the output bucket
    prepared_blobname = 'tables/phl_opa_properties/phl_opa_properties.jsonl'
    blob = output_bucket.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname} in {output_bucket_name}')

    return f'Processed data into {prepared_filename} and uploaded to gs://{output_bucket_name}/{prepared_blobname}'