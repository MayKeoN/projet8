-- stg_cog_region.sql
-- Staging model for INSEE COG region reference table.
--
-- Responsibilities (staging layer: 1-to-1 with source, cleaning only):
--   - Rename columns to snake_case lowercase
--   - TRIM reg_code for safety
--
-- No joins, no business logic.

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
