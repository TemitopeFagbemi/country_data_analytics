{{ config(
    materialized='incremental',
    unique_key='country_name'
) }}

SELECT
    data:name.common::STRING       AS country_name,
    data:region::STRING            AS region,
    CASE 
    WHEN region IN ('Europe') THEN 'Europe'
    WHEN region IN ('Africa') THEN 'Africa'
    WHEN region IN ('Asia') THEN 'Asia'
    WHEN region IN ('Americas') THEN 'Americas'
    WHEN region IN ('Oceania') THEN 'Oceania'
    ELSE 'Other'
END AS continent,
    data:population::NUMBER        AS population,
    data:capital[0]::STRING        AS capital_city,

    -- ✅ SAFE currency extraction
    CASE 
    WHEN data:currencies IS NOT NULL 
         AND ARRAY_SIZE(OBJECT_KEYS(data:currencies)) > 0
    THEN OBJECT_KEYS(data:currencies)[0]::STRING
    ELSE 'NO_CURRENCY'
END AS currency_code,

CASE 
    WHEN data:currencies IS NOT NULL 
         AND ARRAY_SIZE(OBJECT_KEYS(data:currencies)) > 0
    THEN data:currencies[OBJECT_KEYS(data:currencies)[0]].name::STRING
    ELSE 'NO_CURRENCY'
END AS currency_name,

    load_timestamp

FROM {{ source('your_source', 'countries_data_raw') }}

{% if is_incremental() %}
WHERE load_timestamp > (
    SELECT MAX(load_timestamp) FROM {{ this }}
)
{% endif %}

QUALIFY ROW_NUMBER() OVER (
    PARTITION BY country_name
    ORDER BY load_timestamp DESC
) = 1