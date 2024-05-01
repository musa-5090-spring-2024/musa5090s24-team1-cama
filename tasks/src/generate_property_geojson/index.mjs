import 'dotenv' from 'dotenv';
import findConfig from 'find-config';
dotenv.config({path: findConfig('.env')});

import { BigQuery } from '@google-cloud/bigquery';
import { Storage } from '@google-cloud/storage';

const bigqueryClient = new BigQuery();

const sql = `
SELECT
    property.parcel_number      AS id,
    LEFT(property.sale_date, 10) AS last_sale_date,
    property.sale_price         AS last_sale_price,
    ST_ASGEOJSON(parcel.geometry)   AS geometry
FROM phl.opa_properties AS property
JOIN phl.pwd_parcels    AS parcel
    ON LPAD(property.parcel_number, 10, '0') = LPAD(CAST(parcel.BRT_ID AS STRING), 10, '0')
WHERE property.zip_code = '19104'
`;

const queryResults = await bigqueryClient.query(sql);
console.log(`This line is just for a breakpoint.`)