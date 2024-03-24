# Setup Guide for MUSA5090-S24-TEAM1-CAMA ETL Pipeline Subdirectory

Follow these steps to set up the project environment:

## 1. Install pipx
Follow the instructions at https://github.com/pypa/pipx to install pipx.

## 2. Install pyenv
Follow the instructions at https://github.com/pyenv/pyenv to install pyenv.

## 3. Install Poetry
Visit https://python-poetry.org/docs/ for instructions on installing Poetry.

## 4. Clone the GitHub Repository
Clone the git repository to your local machine by running the following command in your command line interface (CLI):

`git clone https://github.com/musa-5090-spring-2024/musa5090s24-team1-cama.git`

## 5. Install Dependencies with Poetry
In your command line interface (CLI), navigate to the `tasks` subdirectory with `cd musa5020s24-team1-cama/tasks` and then run `poetry install`.

## 6. Activate the Virtual Environment
Activate the virtual environment by running:

`poetry shell`

## Setting User Credentials for Google Cloud

### Install and Initialize gcloud CLI

Follow the instructions to [install the gcloud CLI](https://cloud.google.com/sdk/docs/install). Once the CLI is open, it will ask you to log in. Do so with the appropriate account and pick the relevant cloud project=. Your authentication should automatically be saved to your local machine.

Then run `gcloud auth application-default login` to authenticate.

## Running the ETL Script
To run the script, navigate to the `tasks` directory and activate the virtual environment with `poetry shell`. Then, run the main script with. This is done with `python tasks/src/script.py`.