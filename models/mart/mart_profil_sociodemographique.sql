-- mart_profil_sociodemographique.sql
-- Final analytical table: OC student profile vs French general population.
--
-- Grain: one row per (year, region, gender, age_group)
-- Materialized as table for export and Colab analysis.
--
-- gender values: 'M', 'F', 'Non renseigne', 'Total'
--
-- Join strategy:
--   Full outer join on (year, region, age_group) with CASE on gender:
--     M            → joins INSEE gender = 'M'
--     F            → joins INSEE gender = 'F'
--     Non renseigne→ joins INSEE gender = 'Total' (total pop as denominator)
--     Total        → joins INSEE gender = 'Total' (total pop as denominator)
--
--   Corse appears with null student_count (no OC students)
--   Non renseigne appears with Total population as denominator
--
-- Columns:
--   student_count      : OC students in this segment (null if no students)
--   population         : INSEE population for denominator (null if no INSEE match)
--   students_per_100k  : student_count / population * 100000

with students as (

    select * from {{ ref('int_students_by_year_region') }}

),

insee as (

    select * from {{ ref('int_insee_by_year_region') }}
    where age_group_oc not in ('0-4 ans', '5-9 ans', '10-14 ans', '15-19 ans')

),

joined as (

    select
        coalesce(students.year,      insee.year)            as year,
        coalesce(students.region,    insee.region)          as region,
        coalesce(students.gender,    insee.gender)          as gender,
        coalesce(students.age_group, insee.age_group_oc)    as age_group,
        students.student_count,
        insee.population,
        case
            when students.student_count is not null
             and insee.population is not null
             and insee.population > 0
            then round(students.student_count / insee.population * 100000, 2)
            else null
        end                                                 as students_per_100k

    from students
    full outer join insee
        on  students.year      = insee.year
        and students.region    = insee.region
        and students.age_group = insee.age_group_oc
        and case
                when students.gender in ('Non renseigne', 'Total') then 'Total'
                else students.gender
            end                = insee.gender

)

select * from joined
order by year, region, gender, age_group
