{% docs ocr_project__sources_layer %}

Couche **source** (`raw`) : tables chargées par `dbt seed` après conversion Python des fichiers bruts.

Les tests `not_null` sur les clés primaires sont déclarés dans `_src_raw.yml`.
Les tests complets (unique, accepted_values, relationships) sont dans les modèles staging.

{% enddocs %}

{% docs ocr_project__mart_layer %}

Couche **mart** : table analytique finale `mart_profil_sociodemographique`.

Granularité : une ligne par (année, région, genre, tranche d'âge).
Genres : M, F, Non renseigné, Total.
Matérialisée en **table** pour export CSV et analyse Google Colab.

{% enddocs %}
