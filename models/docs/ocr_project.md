{% docs ocr_project__overview %}

# Projet 8 OCR — Profil sociodémographique Data

Pipeline dbt analysant l'evolution du profil des etudiants **parcours Data** OpenClassrooms (2022-2025),
enrichi par les estimations de population INSEE et le referentiel geographique COG.

## Principes

- **Python** : chargement minimal (dump CSV / xlsx vers seeds), sans logique metier.
- **Staging** : miroir 1:1 des sources + nettoyage structural uniquement.
- **Intermediate** : jointures COG, enrichissement INSEE, harmonisation des tranches d'age, agregations.
- **Mart** : table analytique finale avec indicateurs de comparaison INSEE (/ 100 000 habitants).

## RGPD

Donnees pseudonymisees (`USER_ID`). Finalite : analyse sociodemographique **agregee** - pas de donnees nominatives.

## Reproductibilite

```
python scripts/run_all_imports.py
dbtf build
```

{% enddocs %}

{% docs ocr_project__sources_layer %}

Couche **source** (`raw`) : tables chargees par `dbt seed` apres conversion Python des fichiers bruts.

Les tests generiques (`not_null`) sur les cles primaires sont declares dans `_src_raw.yml`.
Les tests complets (unique, accepted_values, relationships) sont dans les modeles staging.

{% enddocs %}

{% docs ocr_project__staging_layer %}

Couche **staging** : renommage snake_case, cast des types, nettoyage structural.

Responsabilites :
- `stg_students` : filtre parcours Data, genre vide -> 'Non renseigne', cast annee en integer
- `stg_insee_population` : filtre agregats geographiques, unpivot format large -> long, strip prefixe genre
- `stg_cog_departement` / `stg_cog_region` : passthrough avec TRIM

Les jointures geographiques et transformations INSEE ne sont **pas** en staging.

{% enddocs %}

{% docs ocr_project__intermediate_layer %}

Couche **intermediate** : jointures inter-sources, agregations preparatoires, harmonisation.

- `int_cog_departement_region` : bridge geographique dep_code -> reg_name
- `int_students_by_year_region` : agregation etudiants par (annee, region, genre, tranche d'age) + ligne Total
- `int_insee_by_year_region` : agregation INSEE par region, mapping labels OC, rollup 60+, ligne Total

{% enddocs %}

{% docs ocr_project__mart_layer %}

Couche **mart** : table analytique finale `mart_profil_sociodemographique`.

Grain : une ligne par (annee, region, genre, tranche d'age).
Genre values : M, F, Non renseigne, Total.
Materialise en **table** pour export CSV et analyse Google Colab.

{% enddocs %}
