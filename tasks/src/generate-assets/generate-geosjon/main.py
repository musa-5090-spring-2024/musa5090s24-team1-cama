from dotenv import load_dotenv
load_dotenv()

import os
import pathlib
from google.cloud import bigquery
from google.cloud import storage
import geojson

import functions_framework


DIRNAME = pathlib.Path(__file__).parent

@functions_framework.http
def generate_property_geojson(team_number):
    # Configure the client with your credentials and project
    bigquery_client = bigquery.Client()
    storage_client = storage.Client()
    bucket_name = os.getenv('TEMP_DATA_LAKE_BUCKET')
    geojson_file_name = "property_tile_info.geojson"

    # Define the query
    query = """
    SELECT p.geometry, p.property_id, p.address, o.tax_year_assessed_value, m.current_assessed_value
    FROM `musa509s24-team1.core.pwd_parcels` p
    JOIN `musa509s24-team1.core.opa_assessments` o ON p.property_id = o.property_id
    JOIN `musa509s24-team1.core.model_predictions` m ON p.property_id = m.property_id
    """


    # Execute the query
    query_job = bigquery_client.query(query)
    results = query_job.result()

    # Construct the GeoJSON
    features = []
    for row in results:
        feature = geojson.Feature(
            geometry=geojson.loads(row.geometry),
            properties={
                "property_id": row.property_id,
                "address": row.address,
                "tax_year_assessed_value": row.tax_year_assessed_value,
                "current_assessed_value": row.current_assessed_value
            }
        )
        features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    # Save to GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(geojson_file_name)
    blob.upload_from_string(geojson.dumps(feature_collection), content_type='application/json')

    print(f"GeoJSON file saved to {bucket_name}/{geojson_file_name}")

    # Print statements for confirmation
    print("Query executed successfully.")
    print("GeoJSON constructed.")
    print("GeoJSON file uploaded to GCS.")
