# Projet 8 — Analyse sociodémographique des étudiants Data OCR

Analyse de l'évolution du profil sociodémographique des étudiants inscrits
aux parcours Data d'OpenClassrooms sur 4 ans (2022–2025).

## Stack technique

| Element | Valeur |
|---------|--------|
| Entrepot | Snowflake (GCP europe-west4, Standard) |
| Transformation | dbt + dbt Fusion Engine (dbtf) |
| Developpement | Cursor (local) + dbt Cloud (docs, CI) |
| Versioning | Git + GitHub |
| Analyse / Visualisation | Google Colab (sur export CSV du mart) |

## Structure du projet

```
projet8/
├── data/               <- fichiers sources bruts (versionnés, non modifies)
├── scripts/            <- conversion des sources brutes en seeds CSV
│   ├── run_all_imports.py
│   ├── prepare_csv_seeds.py
│   └── prepare_insee_seed.py
├── seeds/              <- CSVs generes par les scripts, charges par dbtf build
├── models/
│   ├── docs/           <- blocs de documentation dbt (ocr_*.md)
│   ├── staging/
│   │   ├── _src_raw.yml              <- sources + not_null sur cles primaires
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
│   │   ├── _int_cog.yml
│   │   ├── _int_students.yml
│   │   └── _int_insee.yml
│   └── mart/
│       ├── mart_profil_sociodemographique.sql
│       └── _mart.yml
├── macros/
│   └── generate_schema_name.sql
├── tests/              <- tests singuliers SQL
└── dbt_project.yml
```

## DAG (lineage)

```
seeds/
  students_raw ──────────────────────────────► stg_students
                                                      │
                                          int_students_by_year_region
                                                      │
                                                      ├──────────────────────────────► mart_profil_sociodemographique
                                                      │                                        │
  cog_departement ──► stg_cog_departement ──┐           │                                        └──► (export CSV → Colab)
                                            ├─► int_cog_departement_region
  cog_region ────────► stg_cog_region ──────┘           │
                                                        │
  insee_population_raw ──► stg_insee_population         │
                                    │                   │
                            int_insee_by_year_region ◄──┘
                                    │
                                    └──────────────────────────────────────────────────────────► mart
```

Le référentiel COG sert uniquement à enrichir la branche INSEE (agrégation département → région).
La branche étudiants ne passe pas par COG : la région est déjà renseignée dans la source OCR.

## Strategie de tests

| Couche | Tests |
|--------|-------|
| Source (`_src_raw.yml`) | `not_null` sur la cle primaire uniquement |
| Staging (`_stg_*.yml`) | `not_null`, `unique`, `accepted_values`, `relationships` |
| Intermediate (`_int_*.yml`) | `not_null`, `unique`, `accepted_values` ; `relationships` sur `_int_cog.yml` |
| Tests singuliers (`tests/`) | Regles metier complexes |

## Reproduire le pipeline

### 1. Prerequis

```bash
python -m venv venv
venv\Scripts\activate
pip install dbt-snowflake pandas openpyxl
```

### 2. Configurer le profil dbt

`C:\Users\<user>\.dbt\profiles.yml` (non versionne) :

```yaml
projet8:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: kfnkzzi-ej76874
      user: YAM
      password: <mot de passe>
      role: ACCOUNTADMIN
      warehouse: COMPUTE_WH
      database: PROJET8
      schema: RAW
      threads: 4
      connect_retries: 1
      connect_timeout: 10
```

### 3. Lancer le pipeline complet

```bash
python scripts/run_all_imports.py
dbtf build
```

### 4. Mettre a jour les donnees

```bash
python scripts/run_all_imports.py
dbtf build --full-refresh
```

## RGPD

- `USER_ID` : identifiant technique pseudonymise, non nominatif
- Finalite : analyse sociodemographique agregee (age, genre, region)
- Donnees INSEE : publiques, aucune contrainte RGPD
