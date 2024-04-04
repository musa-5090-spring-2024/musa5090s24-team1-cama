## Making BigQuery tables

```shell
bq mk --dataset --description "External tables backed by prepared source data in Cloud Storage." musa509s24-team1:source
bq mk --dataset --description "Data that is ready to be used for analysis. Mostly copies of external tables." musa509s24-team1:core
bq mk --dataset --description "Data that has been derived from core data. Outputs from analyses or models go here." musa509s24-team1:derived

```