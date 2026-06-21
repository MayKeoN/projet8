-- int_insee_by_year_region.sql
-- Population INSEE agrégée par année, région OC, genre et tranche d'âge.
-- Mapping labels OC par fonctions de chaînes ; tranches 60+ regroupées en '60 ans ou plus'.
-- DOM → DROM ; départements 971-976 exclus (couverts par l'agrégat DOM).
-- Ligne Total = M + F uniquement (INSEE sans catégorie Non renseigné).

with insee as (

    select * from {{ ref('stg_insee_population') }}

),

cog as (

    select * from {{ ref('int_cog_departement_region') }}

),

mapped as (

    select
        insee.year,
        case
            when insee.dep_code = 'DOM' then 'DROM'
            else cog.reg_name
        end                                             as region,
        insee.gender,
        case
            when insee.age_group_insee in (
                '60_a_64_ans', '65_a_69_ans', '70_a_74_ans',
                '75_a_79_ans', '80_a_84_ans', '85_a_89_ans',
                '90_a_94_ans', '95_ans_et_plus'
            ) then '60 ans ou plus'
            else replace(
                    replace(
                        replace(insee.age_group_insee, '_a_', '-'),
                    '_ans', ' ans'),
                '_', ' ')
        end                                             as age_group_oc,
        insee.population

    from insee
    left join cog
        on insee.dep_code = cog.dep_code
    where insee.dep_code not in ('971', '972', '973', '974', '976')

),

aggregated as (

    select
        year,
        region,
        gender,
        age_group_oc,
        sum(population) as population

    from mapped
    where region is not null
    group by 1, 2, 3, 4

),

totals as (

    select
        year,
        region,
        'Total'             as gender,
        age_group_oc,
        sum(population)     as population

    from aggregated
    group by 1, 2, 4

)

select * from aggregated
union all
select * from totals
