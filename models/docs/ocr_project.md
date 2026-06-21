{% docs ocr_project__overview %}

Pipeline dbt analysant l'évolution du profil des étudiants **parcours Data** OpenClassrooms (2022–2025),
enrichi par les estimations de population INSEE et le référentiel géographique COG.

- **Python** : chargement minimal — dump CSV/xlsx vers seeds, sans logique métier.
- **Staging** : miroir 1:1 des sources, nettoyage structural uniquement.
- **Intermediate** : jointures COG, harmonisation des tranches d'âge, agrégations.
- **Mart** : table analytique finale avec indicateurs de comparaison INSEE (/100 000 habitants).

RGPD : `USER_ID` pseudonymisé. Finalité : analyse sociodémographique **agrégée**.

{% enddocs %}

{% docs ocr_project__sources_layer %}

Couche **source** (`raw`) : tables chargées par `dbt seed` après conversion Python des fichiers bruts.

Tests `not_null` sur les clés primaires déclarés dans `_src_raw.yml`.
Tests complets (unique, accepted_values, relationships) dans les modèles staging.

{% enddocs %}

{% docs ocr_project__staging_layer %}

Couche **staging** : renommage snake_case, cast des types, nettoyage structural.

- `stg_students` : filtre parcours Data, genre vide → 'Non renseigné', cast année en integer
- `stg_insee_population` : filtre agrégats géographiques, unpivot format large → long, suppression préfixe genre
- `stg_cog_departement` / `stg_cog_region` : passthrough avec TRIM

Les jointures géographiques ne sont pas en staging.

{% enddocs %}

{% docs ocr_project__intermediate_layer %}

Couche **intermediate** : jointures inter-sources, agrégations préparatoires, harmonisation.

- `int_cog_departement_region` : bridge géographique dep_code → reg_name
- `int_students_by_year_region` : agrégation étudiants par (année, région, genre, tranche d'âge) + ligne Total
- `int_insee_by_year_region` : agrégation INSEE par région, mapping labels OC, rollup 60+, ligne Total

{% enddocs %}

{% docs ocr_project__mart_layer %}

Couche **mart** : table analytique finale `mart_profil_sociodemographique`.

Granularité : une ligne par (année, région, genre, tranche d'âge).
Genres : M, F, Non renseigné, Total.
Matérialisée en **table** pour export CSV et analyse Google Colab.

{% enddocs %}
