{% docs ocr_source__students_raw %}

Inscriptions brutes exportees du SI OpenClassrooms (CSV mission).

Perimetre filtre en staging : parcours **Data**, annees **2022-2025**.

| Colonne | Type | Description |
|---------|------|-------------|
| USER_ID | STRING | Identifiant technique pseudonymise (non nominatif - RGPD) |
| PATH_CATEGORY_NAME | STRING | Categorie du parcours (toujours 'Data' apres filtre) |
| AGE_GROUP | STRING | Tranche d'age au debut du parcours (ex: '25-29 ans') |
| GENDER | STRING | Genre declare - peut etre vide (~27% en 2022, en baisse) |
| REGION | STRING | Region de residence (libelle INSEE ou 'DROM') |
| YEAR_PATH_STARTED | INTEGER | Annee de debut du parcours (2022-2025) |

{% enddocs %}

{% docs ocr_source__insee_population_raw %}

Estimations de population INSEE par departement, sexe et tranche d'age quinquennale.

Source : fichier xlsx `estim-pop-dep-sexe-aq-1975-2025` (onglets 2022-2025).
Aucune agregation en Python - dump brut vers seeds.

Colonnes cles apres conversion :
- `year` : annee de l'estimation
- `dep_code` : code departement ('01' a '976', 'DOM' pour agregat outre-mer)
- `dep_name` : nom du departement (vide pour la ligne agregat DOM)
- `hommes_*` / `femmes_*` : population par tranche d'age quinquennale

{% enddocs %}

{% docs ocr_source__cog_departement %}

Referentiel COG INSEE 2024 - **departements**.

| Colonne | Description |
|---------|-------------|
| DEP | Code departement (zero-padde, ex: '01', '2A', '2B') |
| REG | Code region parente |
| LIBELLE | Libelle officiel du departement |

{% enddocs %}

{% docs ocr_source__cog_region %}

Referentiel COG INSEE 2024 - **regions**.

| Colonne | Description |
|---------|-------------|
| REG | Code region |
| LIBELLE | Libelle officiel (aligne sur les libelles OCR metropole) |

{% enddocs %}
