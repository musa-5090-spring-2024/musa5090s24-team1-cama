import dotenv
dotenv.load_dotenv()

from google.cloud import bigquery
from google.cloud import storage

bigquery_client = bigquery.Client()

sql = '''
    SELECT
            property.parcel_number          AS id,
            LEFT(property.sale_date, 10)    AS last_sale_date,
            property.sale_price             AS last_sale_price,
            ST_ASGEOJSON(parcel.geometry)   AS geometry
        FROM source.opa_properties     AS property
        JOIN source.pwd_parcels        AS parcel
            ON LPAD(property.parcel_number, 10, '0') = LPAD(CAST(parcel.BRT_ID AS STRING), 10, "0")
        WHERE property.zip_code = '19104'
'''

query_results = bigquery_client.query_and_wait(sql)
print('This is a breakpoint.')