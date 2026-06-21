-- mart_profil_sociodemographique.sql
-- Table analytique : profil étudiants OCR vs population générale INSEE.
--
-- Jointure externe complète sur (année, région, tranche d'âge) :
--   M / F                 → population INSEE du même genre
--   Non renseigné / Total → population totale M+F (dénominateur conservateur)
-- Corse : student_count null (aucun étudiant OCR).
-- Tranches INSEE < 20 ans exclues (hors périmètre OCR).

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
            then round(students.student_count / insee.population * 100000, 3)
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
