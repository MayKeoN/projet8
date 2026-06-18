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

## Structure du projet

```
projet8/
├── data/               ← fichiers sources bruts (versionnés, non modifiés)
│   ├── DATASET_-_MAJ_-_P8_-_1040-_DA_-_DATA.csv
│   ├── estim-pop-dep-sexe-aq-1975-2025.xlsx
│   ├── v_departement_2024.csv
│   └── v_region_2024.csv
├── scripts/            ← conversion des sources brutes en seeds CSV
│   ├── run_all_imports.py
│   ├── prepare_students_seed.py
│   ├── prepare_insee_seed.py
│   └── prepare_cog_seeds.py
├── seeds/              ← CSVs générés par les scripts, chargés par dbt build
│   ├── students_raw.csv
│   ├── insee_population_raw.csv
│   ├── cog_departement.csv
│   └── cog_region.csv
├── models/
│   ├── staging/
│   │   ├── openclassrooms/
│   │   └── insee/
│   ├── intermediate/
│   └── mart/
├── tests/              ← tests singuliers SQL
├── analyses/
└── dbt_project.yml
```

## Reproduire le pipeline

### 1. Prérequis

```bash
python -m venv venv
venv\Scripts\activate
pip install dbt-snowflake pandas openpyxl
```

Installer le dbt Fusion Engine (dbtf) :
https://docs.getdbt.com/docs/core/installation-overview

### 2. Configurer le profil dbt

Le fichier `profiles.yml` n'est **pas versionné** (credentials).
Il doit être créé manuellement dans `C:\Users\<user>\.dbt\profiles.yml` :

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
      threads: 1
```

### 3. Lancer le pipeline complet

```bash
# Étape 1 — convertir les sources brutes en seeds CSV
python scripts/run_all_imports.py

# Étape 2 — seed + modèles + tests (tout en un)
dbtf build
```

> `dbtf build` exécute dans l'ordre DAG : seeds → modèles → tests.
> Pas besoin de lancer `dbt seed` séparément.

### 4. Mettre à jour les données

Remplacer le fichier concerné dans `data/`, puis relancer :

```bash
python scripts/run_all_imports.py
dbtf build --full-refresh
```

## RGPD

- `USER_ID` : identifiant technique pseudonymisé, non nominatif
- Finalité : analyse sociodémographique agrégée (âge, genre, région)
- Données INSEE : publiques, aucune contrainte RGPD
