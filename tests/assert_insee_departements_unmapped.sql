-- assert_insee_departements_unmapped.sql
-- Chaque dep_code dans stg_insee_population (hors agrégat 'DOM')
-- doit trouver une correspondance dans stg_cog_departement.
-- Échoue si un département INSEE n'est pas référencé dans le COG.

select distinct i.dep_code
from {{ ref('stg_insee_population') }} i
left join {{ ref('stg_cog_departement') }} d
    on i.dep_code = d.dep_code
where d.dep_code is null
  and i.dep_code != 'DOM'
