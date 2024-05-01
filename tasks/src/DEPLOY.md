## Deploying the Workflow

The steps below will create the necessary resources in Google Cloud to run the workflow. First, we create tasks to extract and prepare PHL OPA properties. We then create a workflow to run these tasks, and finally we create a scheduler to run the workflow on a weekly basis (every Monday at midnight).

### Windows
Assuming you're on a Windows machine, you can run the following commands in PowerShell.

First, in your root directory, make sure your default Google Cloud project is set appropriately (note that it is *not* musa5090s24-team1 here, but rather musa509s24-team1): `gcloud config set project musa509s24-team1`.

Next, navigate to the `tasks/src` directory in this repository.

To create the extract OPA properties task, run the following command:

```shell
gcloud functions deploy extract_phl_opa_properties `
--gen2 `
--region=us-central1 `
--runtime=python312 `
--source=. `
--entry-point=extract_phl_opa_properties `
--service-account=musa509s24-team1@appspot.gserviceaccount.com `
--memory=4Gi `
--timeout=240s `
--set-env-vars=DATA_LAKE_BUCKET=musa5090s24_team1_raw_data `
--trigger-http `
--no-allow-unauthenticated `
--project musa509s24-team1
```

To create the prepare OPA properties task, run the following command:

```shell
gcloud functions deploy prepare_phl_opa_properties `
--gen2 `
--region=us-central1 `
--runtime=python312 `
--source=. `
--entry-point=prepare_phl_opa_properties `
--service-account=musa509s24-team1@appspot.gserviceaccount.com `
--memory=8Gi `
--timeout=480s `
--set-env-vars=INPUT_DATA_LAKE_BUCKET='musa5090s24_team1_raw_data',OUTPUT_DATA_LAKE_BUCKET='musa5090s24_team1_prepared_data' `
--trigger-http `
--no-allow-unauthenticated `
--project musa509s24-team1
```

To deploy the pipeline workflow, run the following command:

```shell
gcloud workflows deploy phl-property-data-pipeline `
--region=us-central1 `
--source=phl-property-data-pipeline.yaml `
--service-account='musa509s24-team1@appspot.gserviceaccount.com'
```

Finally, to create a scheduler to run the workflow on a weekly basis, run the following command:

```shell
gcloud scheduler jobs create http phl-property-data-pipeline `
--schedule='0 0 * * 1' `
--time-zone='America/New_York' `
--location='us-central1' `
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa-344004/locations/us-central1/workflows/phl-property-data-pipeline/executions' `
--oidc-service-account-email='musa509s24-team1@appspot.gserviceaccount.com' `
--oidc-token-audience='https://workflowexecutions.googleapis.com/v1/projects/musa-344004/locations/us-central1/workflows/phl-property-data-pipeline/executions'
```

### macOS/Linux

Assuming you're on a macOS or Linux machine, you can run the following commands in your terminal.

First, in your root directory, make sure your default Google Cloud project is set appropriately (note that it is *not* musa5090s24-team1 here, but rather musa509s24-team1): `gcloud config set project musa509s24-team1`.

Next, navigate to the `tasks/src` directory in this repository.

To create the extract OPA properties task, run the following command:

```shell
gcloud functions deploy extract_phl_opa_properties \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=extract_phl_opa_properties \
--service-account=musa509s24-team1@appspot.gserviceaccount.com \
--memory=4Gi \
--timeout=240s \
--set-env-vars=DATA_LAKE_BUCKET=musa5090s24_team1_raw_data \
--trigger-http \
--no-allow-unauthenticated \
--project musa509s24-team1
```

To create the prepare OPA properties task, run the following command:

```shell
gcloud functions deploy prepare_phl_opa_properties \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=prepare_phl_opa_properties \
--service-account=musa509s24-team1@appspot.gserviceaccount.com \
--memory=8Gi \
--timeout=480s \
--set-env-vars=INPUT_DATA_LAKE_BUCKET='musa5090s24_team1_raw_data',OUTPUT_DATA_LAKE_BUCKET='musa5090s24_team1_prepared_data' \
--trigger-http \
--no-allow-unauthenticated \
--project musa509s24-team1
```

```shell
gcloud functions deploy load_opa_properties \
--gen2 \
--region=us-central1 \
--runtime=python312 \
--source=. \
--entry-point=load_opa_properties \
--service-account=musa509s24-team1@appspot.gserviceaccount.com \
--memory=4Gi \
--timeout=240s \
--trigger-http \
--no-allow-unauthenticated \
--project musa509s24-team1
```

To deploy the pipeline workflow, run the following command:

```shell
gcloud workflows deploy phl-property-data-pipeline \
--region=us-central1 \
--source=phl-property-data-pipeline.yaml \
--service-account='musa509s24-team1@appspot.gserviceaccount.com'
```

Finally, to create a scheduler to run the workflow on a weekly basis, run the following command:

```shell
gcloud scheduler jobs create http phl-property-data-pipeline \
--schedule='0 0 * * 1' \
--time-zone='America/New_York' \
--location='us-central1' \
--uri='https://workflowexecutions.googleapis.com/v1/projects/musa-344004/locations/us-central1/workflows/phl-property-data-pipeline/executions' \
--oidc-service-account-email='musa509s24-team1@appspot.gserviceaccount.com' \
--oidc-token-audience='https://workflowexecutions.googleapis.com/v1/projects/musa-344004/locations/us-central1/workflows/phl-property-data-pipeline/executions'
```