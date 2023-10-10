# This script is intended to do the following:
# 1. Use the same GCP service account key as the main dbt project, located in the .keys folder
# 2. Load any libraries needed to connect to Firestore
# 3. Connect to Firestore, using the service account key and the project ID
# 4. Query Firestore for the data needed for the dbt project
# 5. Load the data into environment variables, using the same naming convention as the dbt project

# Import libraries
import os
import json
import google.cloud
from google.cloud import firestore

# Set the path to the service account key, referring the generic project ENV variable
keyfile_path = '/keys/service-account.json'

# Get the project ID from the service account key
with open(keyfile_path) as f:
    data = json.load(f)
    project_id = data['project_id']

# Set the collection name
collection_name = 'dbt-settings'

# Set the document name
document_name = 'dbt-settings'

# Authenticate and initialize Firestore
db = firestore.Client.from_service_account_json(keyfile_path)

doc_ref = db.collection(collection_name).document(document_name)
doc = doc_ref.get()

# Define a local dictionary to hold the data, and load all available key-value pairs into it.
data = {}
if doc.exists:
    data = doc.to_dict()

# Define a list of the mandatory keys
mandatory_keys = [
    'insentric_schema_version',
    'mkto_table_postfix',
]

# Validate if all mandatory keys are present. Collect the missing keys in a list, and raise an error if any are missing
missing_keys = []
for key in mandatory_keys:
    if key not in data:
        missing_keys.append(key)

if len(missing_keys) > 0:
    raise ValueError('The following mandatory keys are missing from Firestore: ' + ', '.join(missing_keys))

# Push all available data to the environment variables
for key, value in data.items():
    os.environ['DBT_ENV_' + key.upper()] = str(value)

# End of script