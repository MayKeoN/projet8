-- int_students_by_year_region.sql
-- Effectifs étudiants par année, région, genre et tranche d'âge.
-- 'Non renseigne' conservé comme genre valide. Ligne Total = M + F + Non renseigné.

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
