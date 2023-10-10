#!/bin/sh

# Authenticate with service account to enable Cloud Logging
gcloud auth activate-service-account --key-file="/keys/service-account.json"

# Install Google Cloud SDK for Python
pip3 install google-cloud-firestore

# Retrieve values from Firesture using a dedicated Python script.
source ./get_firestore_data.py
echo "Firestore data retrieved"
printenv DBT_ENV_MKTO_TABLE_POSTFIX

# Pulls the most recent version of the dependencies listed in your packages.yml from git
#dbt deps --profiles-dir .

if dbt debug --target cloudrun --profiles-dir .; then
  gcloud logging write dbt-jaffle-shop "dbt debug succeeded"
else
  gcloud logging write dbt-jaffle-shop "dbt debug failed"
fi

if dbt run --target cloudrun --profiles-dir .; then
  gcloud logging write dbt-jaffle-shop "dbt run succeeded"
else
  gcloud logging write dbt-jaffle-shop "dbt run failed"
fi

if dbt test --target cloudrun --profiles-dir .; then
  gcloud logging write dbt-jaffle-shop "dbt test succeeded"
else
  gcloud logging write dbt-jaffle-shop "dbt test failed"
fi