-- stg_cog_departement.sql
-- Référentiel COG INSEE 2024 — départements. Renommage et TRIM des codes.

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
