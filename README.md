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
| Visualisation | Google Colab |

## Structure du projet

```
projet8/
├── data/               ← fichiers sources bruts (versionnés, non modifiés)
├── scripts/            ← conversion des sources en seeds CSV
│   ├── run_all_imports.py
│   ├── prepare_csv_seeds.py
│   └── prepare_insee_seed.py
├── seeds/              ← CSVs normalisés, chargés dans Snowflake par dbtf build
├── models/
│   ├── docs/           ← blocs de documentation dbt
│   ├── staging/        ← nettoyage 1:1, sans jointure
│   ├── intermediate/   ← jointures inter-sources, agrégations
│   └── mart/           ← table analytique finale
├── macros/
├── tests/              ← tests singuliers SQL
├── analyses/           ← notebook Google Colab
└── dbt_project.yml
```

## Reproduire le pipeline

### Prérequis

```bash
python -m venv venv
venv\Scripts\activate
pip install dbt-snowflake pandas openpyxl
```

Créer `~/.dbt/profiles.yml` (non versionné) :

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

### Lancer le pipeline

```bash
python scripts/run_all_imports.py
dbtf build
```

`dbtf build` exécute seeds → modèles → tests dans l'ordre du DAG.

### Mise à jour des données

```bash
python scripts/run_all_imports.py
dbtf build --full-refresh
```

## Tests

| Couche | Tests |
|--------|-------|
| Source | `not_null` sur clé primaire |
| Staging | `not_null`, `unique`, `accepted_values`, `relationships` |
| Intermediate | `not_null`, `unique`, `accepted_values`, `relationships` |
| Mart | `not_null`, `accepted_values` |
| Singuliers | `assert_unique_student_year`, `assert_student_regions_mapped`, `assert_insee_departements_unmapped` |

**Note syntaxe dbtf Fusion Engine** — `accepted_values` requiert `arguments: values:` au lieu de `values:` (différence avec dbt Core).

## Livrables

| # | Livrable |
|---|---------|
| 1 | `mart_profil_sociodemographique.csv` — export Snowflake |
| 2 | Ce repo GitHub — workflow dbt commenté |
| 3 | Support de présentation |

## RGPD

`USER_ID` pseudonymisé, non nominatif. Finalité : analyse sociodémographique agrégée. Données INSEE publiques.
