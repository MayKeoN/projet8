{% docs ocr_glossary__gender %}

Genre de l'étudiant après normalisation en staging.

| Valeur | Définition |
|--------|------------|
| M | Homme (valeur renseignée dans la source OCR) |
| F | Femme (valeur renseignée dans la source OCR) |
| Non renseigné | Champ source vide (~27 % des lignes en 2022, ~7 % en 2025) — aucune imputation (RGPD) |
| Total | Somme M + F + Non renseigné — ligne calculée en intermediate |

L'évolution du taux de genre non renseigné (41 % → 7 %) est un résultat analytique du projet.

{% enddocs %}

{% docs ocr_glossary__age_harmonization %}

Harmonisation des tranches d'âge entre les deux sources :

| Source | Format exemple | Traitement |
|--------|---------------|------------|
| OCR | `25-29 ans` | Référence — pas de transformation |
| INSEE (col. name) | `hommes_25_a_29_ans` | Suppression du préfixe genre en staging, REPLACE en intermediate |
| INSEE 60+ | 8 tranches quinquennales (60-64 à 95+) | Regroupement → `60 ans ou plus` en intermediate |

Le libellé OC est dérivé par fonctions de chaînes (pas de CASE codé en dur),
sauf pour `60 ans ou plus` qui nécessite une agrégation explicite.

{% enddocs %}

{% docs ocr_glossary__insee_penetration %}

Taux d'inscriptions pour **100 000 habitants** (`students_per_100k`).

Calculé dans le mart sur la granularité (année, région, genre, tranche d'âge).

Règles de dénominateur selon le genre :
- **M** : population masculine de la tranche (source INSEE)
- **F** : population féminine de la tranche (source INSEE)
- **Non renseigné** : population totale M+F de la tranche (approche conservative)
- **Total** : population totale M+F de la tranche

La jointure externe complète assure que la Corse (0 étudiant OCR) et
les segments sans correspondance INSEE apparaissent avec des valeurs nulles.

{% enddocs %}
