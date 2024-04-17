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
from shapely.validation import explain_validity

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def prepare_phl_opa_properties(request):
    print('Preparing OPA Properties data...')

    raw_filename = DIRNAME / 'opa_properties_public.geojson'
    prepared_filename = DIRNAME / 'phl_opa_properties.jsonl'

    # Download the data from the input bucket
    raw_blobname = 'raw/phl_opa_properties/phl_opa_properties.geojson'
    prepared_blobname = 'tables/phl_opa_properties/phl_opa_properties.jsonl'
    
    bucket_name = os.getenv('INPUT_DATA_LAKE_BUCKET')
    output_bucket_name = os.getenv('OUTPUT_DATA_LAKE_BUCKET')
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)
    output_bucket = storage_client.bucket(output_bucket_name)

    blob = input_bucket.blob(raw_blobname)
    blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the data from the geojson file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set up the projection
    transformer = pyproj.Transformer.from_proj('epsg:2272', 'epsg:4326', always_xy=True)

    # Process each feature in the GeoJSON and write to JSONL
    prepared_filename = DIRNAME / 'phl_opa_properties.jsonl'
    with open(prepared_filename, 'w') as ofp:
        for feature in geojson_data['features']:
            output_feature = feature['properties']

            # Transform the geometry and convert to GeoJSON format
            geom = shape(feature['geometry'])
            transformed_geom = transform(transformer.transform, geom)
            transformed_geojson = mapping(transformed_geom)

            # Validate the transformed geometry using Shapely
            if not transformed_geom.is_valid:
                print(f"Invalid geometry found, skipping feature ID {output_feature.get('id', 'Unknown')}: {explain_validity(transformed_geom)}")
                continue

            # Serialize the geometry object to a JSON string
            output_feature['geometry'] = json.dumps(transformed_geojson)

            # Write the feature as a JSONL string
            json.dump(output_feature, fp=ofp)
            ofp.write('\n')  # newline for JSONL format

    print(f'Processed data into {prepared_filename}')

    blob = output_bucket.blob(prepared_blobname)
    blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname} in {output_bucket_name}')

    return f'Processed data into {prepared_filename} and uploaded to gs://{output_bucket_name}/{prepared_blobname}'