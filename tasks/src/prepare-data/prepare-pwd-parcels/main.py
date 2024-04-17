from dotenv import load_dotenv
load_dotenv()

import json
import os
import pathlib
from google.cloud import storage
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform
import functions_framework
from shapely.validation import explain_validity

DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def prepare_phl_pwd_parcels(request):
    print('Preparing PWD Parcels data...')

    # Environment setup
    bucket_name = os.getenv('INPUT_DATA_LAKE_BUCKET')
    output_bucket_name = os.getenv('OUTPUT_DATA_LAKE_BUCKET')

    # File and blob setup
    raw_blobname = 'raw/phl_pwd_parcels/phl_pwd_parcels.geojson'
    prepared_blobname = 'tables/phl_pwd_parcels/phl_pwd_parcels.jsonl'

    # Initialize Cloud Storage client
    storage_client = storage.Client()
    input_bucket = storage_client.bucket(bucket_name)
    output_bucket = storage_client.bucket(output_bucket_name)

    # Download the raw GeoJSON file
    raw_blob = input_bucket.blob(raw_blobname)
    raw_filename = DIRNAME / 'phl_pwd_parcels.geojson'
    raw_blob.download_to_filename(raw_filename)
    print(f'Downloaded to {raw_filename}')

    # Load the GeoJSON file
    with open(raw_filename, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Set up the coordinate transformation
    transformer = pyproj.Transformer.from_crs("epsg:2272", "epsg:4326", always_xy=True)

    # Process each feature in the GeoJSON and write to JSONL
    prepared_filename = DIRNAME / 'phl_pwd_parcels.jsonl'
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

    # Upload the prepared JSONL file to Cloud Storage
    prepared_blob = output_bucket.blob(prepared_blobname)
    prepared_blob.upload_from_filename(prepared_filename)
    print(f'Uploaded to {prepared_blobname} in {output_bucket_name}')

    return f'Processed data into {prepared_filename} and uploaded to gs://{output_bucket_name}/{prepared_blobname}', 200
