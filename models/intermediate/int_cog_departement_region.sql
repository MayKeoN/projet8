-- int_cog_departement_region.sql
-- Intermediate model: geographic bridge table.
--
-- Joins COG departement to COG region to produce a single lookup:
--   dep_code → reg_code → reg_name
--
-- Used by:
--   - int_students_enriched (region name matching)
--   - int_insee_by_year_region (dep_code → region aggregation)

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
