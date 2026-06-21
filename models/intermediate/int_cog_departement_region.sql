-- int_cog_departement_region.sql
-- Table de correspondance géographique : dep_code → reg_code → reg_name.
-- Utilisée par int_insee_by_year_region pour agréger la population par région.

with departments as (

    select * from {{ ref('stg_cog_departement') }}

),

regions as (

    select * from {{ ref('stg_cog_region') }}

),

joined as (

    select
        departments.dep_code,
        departments.dep_name,
        departments.reg_code,
        regions.reg_name

    from departments
    left join regions
        on departments.reg_code = regions.reg_code

)

select * from joined
