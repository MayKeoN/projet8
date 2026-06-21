{% docs ocr_glossary__gender %}

Genre de l'etudiant apres normalisation en staging.

| Valeur | Definition |
|--------|------------|
| M | Homme (valeur renseignee dans la source OCR) |
| F | Femme (valeur renseignee dans la source OCR) |
| Non renseigne | Champ source vide (~27% des lignes en 2022, ~7% en 2025) - aucune imputation (RGPD) |
| Total | Somme M + F + Non renseigne - ligne calculee en intermediate |

Le taux de genre non renseigne est un indicateur de qualite de donnee en soi,
son evolution positive (41% -> 7%) est un resultat analytique du projet.

{% enddocs %}

{% docs ocr_glossary__drom %}

**DROM** : libelle region dans le fichier etudiants regroupant les departements d'outre-mer
(Guadeloupe, Martinique, Guyane, La Reunion, Mayotte).

Traitement pipeline :
- Cote etudiants : `region = 'DROM'` conserve tel quel depuis la source
- Cote INSEE : ligne agregat `dep_code = 'DOM'` utilisee (population totale outremer)
- Le CASE SQL `dep_code = 'DOM' -> 'DROM'` assure le mapping en intermediate

Les effectifs etudiants DROM sont conserves et inclus dans toutes les agregations.
Le taux `students_per_100k` est calcule avec la population DOM comme denominateur.

{% enddocs %}

{% docs ocr_glossary__age_harmonization %}

Harmonisation des tranches d'age entre les deux sources :

| Source | Format exemple | Traitement |
|--------|---------------|------------|
| OCR | `25-29 ans` | Reference - pas de transformation |
| INSEE (col. name) | `hommes_25_a_29_ans` | Strip prefixe genre en staging, REPLACE en intermediate |
| INSEE 60+ | 8 tranches quinquennales (60-64 a 95+) | Rollup -> `60 ans ou plus` en intermediate |

Le mapping OC label est derive mecaniquement par string functions (pas de CASE code en dur)
sauf pour la tranche `60 ans ou plus` qui necessite une agregation explicite.

{% enddocs %}

{% docs ocr_glossary__insee_penetration %}

Taux d'inscriptions pour **100 000 habitants** (`students_per_100k`).

Calcule dans le mart sur le grain (annee, region, genre, tranche d'age).

Regles de denominateur selon le genre :
- **M** : population masculine de la tranche (source INSEE)
- **F** : population feminine de la tranche (source INSEE)
- **Non renseigne** : population totale M+F de la tranche (approche conservative)
- **Total** : population totale M+F de la tranche

La jointure FULL OUTER assure que Corse (0 etudiants OCR) et
les segments sans correspondance INSEE apparaissent avec des valeurs nulles.

{% enddocs %}

{% docs ocr_glossary__pipeline_layers %}

Le pipeline suit l'architecture ELT standard avec dbt :

**E - Extract** : fichiers bruts (CSV OCR, XLSX INSEE, CSV COG) dans `data/`
**L - Load** : scripts Python -> seeds CSV -> `dbt seed` -> schéma RAW Snowflake
**T - Transform** : modeles dbt en 3 couches (staging -> intermediate -> mart)

Cette separation garantit la reproductibilite :
un `dbtf build` depuis les seeds reconstruit tout le pipeline de bout en bout.

{% enddocs %}
