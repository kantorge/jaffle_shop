#!/bin/sh
dbt deps --profiles-dir .  # Pulls the most recent version of the dependencies listed in your packages.yml from git
dbt debug --target cloudrun --profiles-dir .
dbt run --target cloudrun --profiles-dir .
dbt test --target cloudrun --profiles-dir .