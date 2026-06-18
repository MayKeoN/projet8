-- stg_cog_departement.sql
-- Staging model for INSEE COG departement reference table.
--
-- Responsibilities (staging layer: 1-to-1 with source, cleaning only):
--   - Rename columns to snake_case lowercase
--   - TRIM dep_code and reg_code for safety
--
-- No joins, no business logic. Jointure with cog_region in intermediate layer.

with source as (

    select * from {{ source('raw', 'cog_departement') }}

),

cleaned as (

    select
        trim(DEP)     as dep_code,
        trim(REG)     as reg_code,
        LIBELLE       as dep_name

    from source

)

select * from cleaned
