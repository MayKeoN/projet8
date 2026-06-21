-- assert_unique_student_year.sql
-- Singular test: each student (user_id) should appear at most once per year.
-- The dataset is longitudinal — a student CAN appear across multiple years,
-- but never twice in the same year (that would be a true duplicate).
--
-- Fails if any (user_id, year_path_started) pair appears more than once.

select
    user_id,
    year_path_started,
    count(*) as n

from {{ ref('stg_students') }}

group by 1, 2

having count(*) > 1
