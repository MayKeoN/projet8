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

## Structure du projet

```
projet8/
├── data/               <- fichiers sources bruts (versionnés, non modifies)
│   ├── DATASET+-+MAJ+-+...csv
│   ├── estim-pop-dep-sexe-aq-1975-2025.xlsx
│   ├── v_departement_2024.csv
│   └── v_region_2024.csv
├── scripts/            <- conversion des sources brutes en seeds CSV
│   ├── run_all_imports.py
│   ├── prepare_csv_seeds.py
│   └── prepare_insee_seed.py
├── seeds/              <- CSVs generes par les scripts, charges par dbtf build
│   ├── students_raw.csv
│   ├── insee_population_raw.csv
│   ├── cog_departement.csv
│   └── cog_region.csv
├── models/
│   ├── staging/
│   │   ├── _src_raw.yml              <- declaration sources + not_null sur cles
│   │   ├── openclassrooms/
│   │   │   ├── stg_students.sql
│   │   │   └── _stg_students.yml
│   │   └── insee/
│   │       ├── stg_cog_departement.sql
│   │       ├── stg_cog_region.sql
│   │       ├── stg_insee_population.sql
│   │       └── _stg_cog.yml
│   ├── intermediate/
│   └── mart/
├── macros/
│   └── generate_schema_name.sql     <- schema naming override (RAW_staging -> STAGING)
├── tests/              <- tests singuliers SQL
└── dbt_project.yml
```

## Strategie de tests

| Couche | Tests |
|--------|-------|
| Source (`_src_raw.yml`) | `not_null` sur la cle primaire de chaque table uniquement |
| Staging (`_stg_*.yml`) | `not_null`, `unique`, `accepted_values`, `relationships` |
| Intermediate | `not_null` sur agregats cles |
| Tests singuliers (`tests/`) | Regles metier complexes (assert_unique_student_year, etc.) |

## Reproduire le pipeline

### 1. Prerequis

```bash
python -m venv venv
venv\Scripts\activate
pip install dbt-snowflake pandas openpyxl
```

Installer le dbt Fusion Engine (dbtf) :
https://docs.getdbt.com/docs/core/installation-overview

### 2. Configurer le profil dbt

Le fichier `profiles.yml` n'est **pas versionne** (credentials).
Le creer manuellement dans `C:\Users\<user>\.dbt\profiles.yml` :

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
# Etape 1 — convertir les sources brutes en seeds CSV
python scripts/run_all_imports.py

# Etape 2 — seed + modeles + tests (tout en un)
dbtf build
```

> `dbtf build` execute dans l'ordre DAG : seeds -> modeles -> tests.
> Pas besoin de lancer `dbt seed` separement.

### 4. Mettre a jour les donnees

Remplacer le fichier concerne dans `data/`, puis relancer :

```bash
python scripts/run_all_imports.py
dbtf build --full-refresh
```

## Note dbtf Fusion

dbtf requiert la syntaxe `arguments: values:` pour `accepted_values` :

```yaml
# Correct (dbtf Fusion)
- accepted_values:
    arguments:
      values: ['Data']

# Incorrect (dbt Core ancien)
- accepted_values:
    values: ['Data']
```

## RGPD

- `USER_ID` : identifiant technique pseudonymise, non nominatif
- Finalite : analyse sociodemographique agregee (age, genre, region)
- Donnees INSEE : publiques, aucune contrainte RGPD
