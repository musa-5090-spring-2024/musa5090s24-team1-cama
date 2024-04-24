# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for tippecanoe
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libsqlite3-dev \
    zlib1g-dev \
    && git clone https://github.com/mapbox/tippecanoe.git \
    && cd tippecanoe \
    && make \
    && make install

# Copy the local code to the container image
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV GOOGLE_CLOUD_PROJECT=musa509s24-team1
ENV INPUT_DATA_LAKE_BUCKET=musa5090s24_team1_raw_data
ENV OUTPUT_DATA_LAKE_BUCKET=musa5090s24_team1_prepared_data
ENV TEMP_DATA_LAKE_BUCKET=musa5090s24_team1_temp_data

# Run the application
CMD ["python", "main.py"]
