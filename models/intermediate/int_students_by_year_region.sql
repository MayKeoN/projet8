-- int_students_by_year_region.sql
-- Intermediate model: OC students aggregated by year, region, gender and age group.
--
-- Responsibilities:
--   - Aggregate student headcount from stg_students
--   - Group by all demographic dimensions needed for the mart join
--   - Preserve 'Non renseigne' gender as a valid dimension value
--   - Add a 'Total' gender row per (year, region, age_group) = M + F + Non renseigne
--
-- Output: one row per (year, region, gender, age_group)
-- gender values: 'M', 'F', 'Non renseigne', 'Total'
-- Used by: mart_profil_sociodemographique

with students as (

    select * from {{ ref('stg_students') }}

),

aggregated as (

    select
        year_path_started   as year,
        region,
        gender,
        age_group,
        count(*)            as student_count

    from students
    group by 1, 2, 3, 4

),

totals as (

    select
        year,
        region,
        'Total'             as gender,
        age_group,
        sum(student_count)  as student_count

    from aggregated
    group by 1, 2, 4

)

select * from aggregated
union all
select * from totals
