-- macros/generate_schema_name.sql
-- Override dbt's default schema naming behaviour.
--
-- By default dbt concatenates the target schema with the custom schema:
--   RAW + staging = RAW_staging
--
-- This macro makes dbt use the custom schema name directly when defined,
-- so models land in STAGING, INTERMEDIATE, MART instead of RAW_staging etc.

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}

{%- endmacro %}
