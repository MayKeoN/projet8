-- stg_students.sql
-- Inscriptions parcours Data OCR (2022-2025).
-- Genre vide remplacé par 'Non renseigne' sans imputation. Filtre PATH_CATEGORY_NAME = 'Data'.

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
