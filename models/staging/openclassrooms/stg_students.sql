-- stg_students.sql
-- Staging model for OpenClassrooms student enrollments.
--
-- Responsibilities (staging layer: 1-to-1 with source, cleaning only):
--   - Rename columns to snake_case
--   - Cast year to integer
--   - Replace empty gender with 'Non renseigne' (not null, not imputed)
--   - Filter to PATH_CATEGORY_NAME = 'Data' (project scope)
--
-- No joins, no aggregations. All business logic in intermediate layer.

with source as (

    select * from {{ source('raw', 'students_raw') }}

),

cleaned as (

    select
        USER_ID                                             as user_id,
        PATH_CATEGORY_NAME                                  as path_category_name,
        AGE_GROUP                                           as age_group,
        coalesce(nullif(trim(GENDER), ''), 'Non renseigne') as gender,
        REGION                                              as region,
        cast(YEAR_PATH_STARTED as integer)                  as year_path_started

    from source

    where PATH_CATEGORY_NAME = 'Data'

)

select * from cleaned
