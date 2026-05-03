{{ config(materialized='table') }}

WITH base AS (
    SELECT *
    FROM {{ ref('countries_silver') }}
),

gdp AS (
    SELECT *
    FROM COUNTRY_DB.PUBLIC.COUNTRY_GDP
),

joined AS (
    SELECT
        b.*,
        g.gdp_usd
    FROM base b
    LEFT JOIN gdp g
        ON b.country_name = g.country_name
),

aggregated AS (
    SELECT
        continent,
        COUNT(*) AS country_count,
        SUM(population) AS total_population,
        AVG(population) AS avg_population,
        SUM(gdp_usd) AS total_gdp
    FROM joined
    GROUP BY continent
)

SELECT *
FROM aggregated





























-- {{ config(materialized='table') }}

-- WITH base AS (
--     SELECT *
--     FROM {{ ref('countries_silver') }}
-- ),

-- aggregated AS (
--     SELECT
--         region,
--         COUNT(*) AS country_count,
--         SUM(population) AS total_population,
--         AVG(population) AS avg_population,
--         MAX(population) AS max_population
--     FROM base
--     GROUP BY region
-- ),

-- largest_country AS (
--     SELECT
--         region,
--         country_name AS largest_country,
--         population
--     FROM base
--     QUALIFY ROW_NUMBER() OVER (
--         PARTITION BY region
--         ORDER BY population DESC
--     ) = 1
-- )

-- SELECT
--     a.region,
--     a.country_count,
--     a.total_population,
--     a.avg_population,
--     l.largest_country,
--     l.population AS largest_country_population

-- FROM aggregated a
-- LEFT JOIN largest_country l
--     ON a.region = l.region






-- -- {{ config(materialized='table') }}

-- -- SELECT
-- --     region,
-- --     COUNT(*) AS country_count,
-- --     SUM(population) AS total_population,
-- --     AVG(population) AS avg_population
-- -- FROM {{ ref('countries_silver') }}
-- -- GROUP BY region