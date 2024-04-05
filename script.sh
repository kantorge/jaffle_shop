#!/bin/bash

# Pulls the most recent version of the dependencies listed in your packages.yml from git
#dbt deps --profiles-dir .

# Install Google Cloud SDK for Python (Firesture and Logging)
pip3 install google-cloud-firestore
pip3 install google-cloud-logging

# Run the main Python script to retrieve Firestore data and to run dbt
python3 ./main.py
