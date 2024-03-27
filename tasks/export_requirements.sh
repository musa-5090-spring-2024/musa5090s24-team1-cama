#!/bin/sh

# Navigate to the tasks directory
cd "$(dirname "$0")"

# Export requirements.txt using Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes
