### Allow cross origin resorce sharing on the public bucket
```bash
gcloud storage buckets update gs://musa5090s24_team1_public --cors-file=public-cors.json

# Check that it went ok
gcloud storage buckets describe gs://musa5090s24_team1_public --format="default(cors_config)"
```
