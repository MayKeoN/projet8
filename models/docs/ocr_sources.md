{% docs ocr_source__students_raw %}

Inscriptions brutes exportées du SI OpenClassrooms (CSV mission).

Périmètre filtré en staging : parcours **Data**, années **2022-2025**.

| Colonne | Type | Description |
|---------|------|-------------|
| USER_ID | STRING | Identifiant technique pseudonymisé (RGPD) |
| PATH_CATEGORY_NAME | STRING | Catégorie du parcours (toujours 'Data' après filtre) |
| AGE_GROUP | STRING | Tranche d'âge au début du parcours (ex. '25-29 ans') |
| GENDER | STRING | Genre déclaré — peut être vide (~27 % en 2022, en baisse) |
| REGION | STRING | Région de résidence (libellé INSEE ou 'DROM') |
| YEAR_PATH_STARTED | INTEGER | Année de début du parcours (2022-2025) |

{% enddocs %}

{% docs ocr_source__insee_population_raw %}

Estimations de population INSEE par département, sexe et tranche d'âge quinquennale.

Source : fichier xlsx `estim-pop-dep-sexe-aq-1975-2025` (onglets 2022-2025).
Export brut vers seeds — aucune agrégation en Python.

Colonnes clés après conversion :
- `year` : année de l'estimation
- `dep_code` : code département ('01' à '976', 'DOM' pour agrégat outre-mer)
- `dep_name` : nom du département (vide pour la ligne DOM)
- `hommes_*` / `femmes_*` : population par tranche d'âge quinquennale

{% enddocs %}

{% docs ocr_source__cog_departement %}

Référentiel COG INSEE 2024 — **départements**.

| Colonne | Description |
|---------|-------------|
| DEP | Code département (complété par des zéros, ex. '01', '2A', '2B') |
| REG | Code région parente |
| LIBELLE | Libellé officiel du département |

{% enddocs %}

{% docs ocr_source__cog_region %}

Référentiel COG INSEE 2024 — **régions**.

| Colonne | Description |
|---------|-------------|
| REG | Code région |
| LIBELLE | Libellé officiel (aligné sur les libellés OCR métropole) |

{% enddocs %}
