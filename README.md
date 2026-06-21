# Projet 8 — Analyse sociodémographique des étudiants Data OCR

Analyse de l'évolution du profil sociodémographique des étudiants inscrits
aux parcours Data d'OpenClassrooms sur 4 ans (2022–2025).

## Stack technique

| Élément | Valeur |
|---------|--------|
| Entrepôt | Snowflake (GCP europe-west4, Standard) |
| Transformation | dbt + dbt Fusion Engine (dbtf) |
| Développement | Cursor (local) + dbt Cloud (docs, CI) |
| Versioning | Git + GitHub |
| Analyse / Visualisation | Google Colab |

## Structure du projet

```
projet8/
├── data/               ← fichiers sources bruts (versionnés, non modifiés)
│   ├── DATASET+-+MAJ+-+...csv       ← données étudiants OCR
│   ├── estim-pop-dep-sexe-aq-1975-2025.xlsx  ← estimations INSEE
│   ├── v_departement_2024.csv       ← référentiel COG départements
│   └── v_region_2024.csv            ← référentiel COG régions
├── scripts/            ← conversion des sources brutes en seeds CSV
│   ├── run_all_imports.py           ← orchestrateur (lancer celui-ci)
│   ├── prepare_csv_seeds.py         ← 3 CSV → students_raw, cog_dep, cog_reg
│   └── prepare_insee_seed.py        ← XLSX INSEE → insee_population_raw
├── seeds/              ← CSVs générés, chargés dans Snowflake par dbtf build
├── models/
│   ├── docs/                        ← blocs de documentation dbt
│   ├── staging/
│   │   ├── _src_raw.yml             ← déclaration sources + tests not_null
│   │   ├── openclassrooms/
│   │   │   ├── stg_students.sql
│   │   │   └── _stg_students.yml
│   │   └── insee/
│   │       ├── stg_cog_departement.sql
│   │       ├── stg_cog_region.sql
│   │       ├── stg_insee_population.sql
│   │       ├── _stg_cog.yml
│   │       └── _stg_insee_population.yml
│   ├── intermediate/
│   │   ├── int_cog_departement_region.sql
│   │   ├── int_students_by_year_region.sql
│   │   ├── int_insee_by_year_region.sql
│   │   └── _int_*.yml
│   └── mart/
│       ├── mart_profil_sociodemographique.sql
│       └── _mart.yml
├── macros/
│   └── generate_schema_name.sql     ← override naming (STAGING vs RAW_staging)
├── tests/
│   └── assert_unique_student_year.sql  ← test singulier longitudinal
├── analyses/
│   └── projet8_colab_analysis.ipynb   ← notebook Google Colab
└── dbt_project.yml
```

## Reproduire le pipeline

### Prérequis

```bash
python -m venv venv
venv\Scripts\activate
pip install dbt-snowflake pandas openpyxl
```

Créer `~/.dbt/profiles.yml` (non versionné — contient les credentials) :

```yaml
projet8:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <account_identifier>
      user: <username>
      password: <password>
      role: ACCOUNTADMIN
      warehouse: COMPUTE_WH
      database: PROJET8
      schema: RAW
      threads: 4
      connect_retries: 1
      connect_timeout: 10
```

### Pipeline complet

```bash
# Étape 1 — convertir les sources brutes en seeds CSV
python scripts/run_all_imports.py

# Étape 2 — seed + modèles + tests
dbtf build
```

`dbtf build` exécute dans l'ordre DAG : seeds → modèles → tests. Une seule commande reconstruit tout.

### Mise à jour des données

```bash
python scripts/run_all_imports.py
dbtf build --full-refresh
```

## Stratégie de tests

| Couche | Tests appliqués |
|--------|----------------|
| Source | `not_null` sur clé primaire uniquement |
| Staging | `not_null`, `unique`, `accepted_values`, `relationships` |
| Intermediate | `not_null`, `unique`, `accepted_values`, `relationships` |
| Mart | `not_null`, `accepted_values` |
| Singulier | `assert_unique_student_year` — données longitudinales |

### Note syntaxe dbtf Fusion Engine

```yaml
# Syntaxe requise par dbtf (différente de dbt Core)
- accepted_values:
    arguments:
      values: ['Data']
```

## Livrables

| # | Livrable | Fichier |
|---|---------|---------|
| 1 | CSV consolidé | `mart_profil_sociodemographique.csv` (export Snowflake) |
| 2 | Workflow dbt | Ce repo GitHub |
| 3 | Présentation | `Projet8_OCR_Presentation.pptx` |

## RGPD

- `USER_ID` : identifiant pseudonymisé, non nominatif
- Finalité : analyse sociodémographique agrégée uniquement
- Données INSEE : publiques, aucune contrainte RGPD
