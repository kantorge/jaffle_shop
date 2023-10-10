# This script is intended to do the following:
# 1. Use the same GCP service account key as the main dbt project, located in the .keys folder
# 2. Load any libraries needed to connect to Firestore
# 3. Connect to Firestore, using the service account key and the project ID
# 4. Query Firestore for the data needed for the dbt project
# 5. As a test, print the data to the console

# Import libraries
import os
import json
import google.cloud
from google.cloud import firestore

# Set the path to the service account key, referring the generic project ENV variable
#keyfile_path = os.getenv('DBT_ENV_GCP_INSENTRIC_KEYFILE_DEV')
keyfile_path = '/keys/service-account.json'

# Set the project ID, referring the generic project ENV variable
#project_id = os.getenv('DBT_ENV_GCP_INSENTRIC_PROJECT_DEV')
project_id = 'beaming-might-304113'

# Set the collection name
#collection_name = 'reports'
collection_name = 'kestra-test'

# Set the document name
#document_name = 'sample-report'
document_name = 'custom-document'

# Authenticate and initialize Firestore
db = firestore.Client.from_service_account_json(keyfile_path)

# Create a reference to the collection
col_ref = db.collection(collection_name)

# Create a query against the collection
query_ref = col_ref#.where(u'field2', u'==', 'value2')

# Get the documents in the collection that match the query
docs = query_ref.stream()

# Print the data to the console
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

print(os.getenv('DBT_PY_TEST'))
os.environ['DBT_PY_TEST'] = '2'
print(os.getenv('DBT_PY_TEST'))

# End of script