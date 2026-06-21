-- assert_student_regions_mapped.sql
-- Chaque région dans stg_students doit être soit une région COG valide, soit 'DROM'.
-- Échoue si une région ne correspond à aucun libellé COG et n'est pas DROM.

select distinct s.region
from {{ ref('stg_students') }} s
left join {{ ref('stg_cog_region') }} r
    on s.region = r.reg_name
where r.reg_name is null
  and s.region != 'DROM'
