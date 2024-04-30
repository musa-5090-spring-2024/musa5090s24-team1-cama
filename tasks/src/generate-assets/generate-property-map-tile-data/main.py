from flask import Flask, request
import subprocess
import tempfile
from google.cloud import storage

app = Flask(__name__)

@app.route('/generate-vector-tiles', methods=['POST'])
def generate_vector_tiles():
    storage_client = storage.Client()
    bucket_name = 'your-bucket-name'
    geojson_file_name = "property_tile_info.geojson"
    output_tile_file = "tiles.mbtiles"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(geojson_file_name)
    with tempfile.NamedTemporaryFile() as temp_geojson:
        blob.download_to_filename(temp_geojson.name)
        with tempfile.NamedTemporaryFile() as temp_mbtiles:
            command = [
                "tippecanoe",
                "-Z", "10",  # Minimum zoom level
                "-z", "15",  # Maximum zoom level
                "-o", temp_mbtiles.name,  # Output file
                temp_geojson.name  # Input GeoJSON file
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print("Vector tiles created successfully.")
                output_blob = bucket.blob(output_tile_file)
                output_blob.upload_from_filename(temp_mbtiles.name)
                return "Vector tiles created and uploaded successfully.", 200
            else:
                print("Failed to create vector tiles.")
                print("Error:", result.stderr)
                return "Failed to create vector tiles.", 500

    return "Unexpected error occurred.", 500
