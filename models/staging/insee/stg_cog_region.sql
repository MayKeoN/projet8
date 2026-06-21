-- stg_cog_region.sql
-- Référentiel COG INSEE 2024 — régions. Renommage et TRIM des codes.

with source as (

    select * from {{ source('raw', 'cog_region') }}

),

cleaned as (

    select
        trim(REG)     as reg_code,
        LIBELLE       as reg_name

    from source

)

select * from cleaned
