-- stg_insee_population.sql
-- Staging model for INSEE population estimates.
--
-- Responsibilities (staging layer):
--   - Filter out aggregate rows with empty dep_code (France metropolitaine, France entiere)
--   - Keep DOM aggregate row (dep_code = 'DOM') — maps to OCR's DROM region
--   - Keep all real department rows including DOM individual departments (971-976)
--   - TRIM dep_code and dep_name
--   - Cast year to integer, population values to integer
--   - Unpivot wide format (63 age band columns) to long format:
--     one row per (year, dep_code, gender, age_group_raw)
--   - Keep all age bands intact — aggregation of 60+ happens in intermediate
--
-- Note: dep_name is empty for the DOM aggregate row (dep_code = 'DOM') by design.

with source as (

    select * from {{ source('raw', 'insee_population_raw') }}

),

-- Keep real departments + DOM aggregate, drop France metropolitaine aggregates
departments_only as (

    select *
    from source
    where dep_code is not null
      and dep_code != ''

),

-- Unpivot hommes columns
hommes as (

    select
        cast(year as integer)       as year,
        trim(dep_code)              as dep_code,
        trim(dep_name)              as dep_name,
        'M'                         as gender,
        age_group_raw,
        cast(population as integer) as population
    from departments_only
    unpivot (population for age_group_raw in (
        hommes_0_a_4_ans,
        hommes_5_a_9_ans,
        hommes_10_a_14_ans,
        hommes_15_a_19_ans,
        hommes_20_a_24_ans,
        hommes_25_a_29_ans,
        hommes_30_a_34_ans,
        hommes_35_a_39_ans,
        hommes_40_a_44_ans,
        hommes_45_a_49_ans,
        hommes_50_a_54_ans,
        hommes_55_a_59_ans,
        hommes_60_a_64_ans,
        hommes_65_a_69_ans,
        hommes_70_a_74_ans,
        hommes_75_a_79_ans,
        hommes_80_a_84_ans,
        hommes_85_a_89_ans,
        hommes_90_a_94_ans,
        hommes_95_ans_et_plus
    ))

),

-- Unpivot femmes columns
femmes as (

    select
        cast(year as integer)       as year,
        trim(dep_code)              as dep_code,
        trim(dep_name)              as dep_name,
        'F'                         as gender,
        age_group_raw,
        cast(population as integer) as population
    from departments_only
    unpivot (population for age_group_raw in (
        femmes_0_a_4_ans,
        femmes_5_a_9_ans,
        femmes_10_a_14_ans,
        femmes_15_a_19_ans,
        femmes_20_a_24_ans,
        femmes_25_a_29_ans,
        femmes_30_a_34_ans,
        femmes_35_a_39_ans,
        femmes_40_a_44_ans,
        femmes_45_a_49_ans,
        femmes_50_a_54_ans,
        femmes_55_a_59_ans,
        femmes_60_a_64_ans,
        femmes_65_a_69_ans,
        femmes_70_a_74_ans,
        femmes_75_a_79_ans,
        femmes_80_a_84_ans,
        femmes_85_a_89_ans,
        femmes_90_a_94_ans,
        femmes_95_ans_et_plus
    ))

)

select * from hommes
union all
select * from femmes
