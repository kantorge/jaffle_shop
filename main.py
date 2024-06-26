# This script is intended to do the following:
# 1. Use the GCP service account key from the Secret Manager, located in the /keys/ folder
# 2. Load any libraries needed to connect to Firestore
# 3. Connect to Firestore, using the service account key and the project ID
# 4. Query Firestore for the data needed for the dbt project
# 5. Load the data into environment variables, using the same naming convention as the dbt project
# 6. Run the dbt project scripts
# 7. Log to GCP based on the dbt results

# Import libraries
import dbt
import os
import json
import google.cloud
from google.cloud import firestore
from google.cloud import logging
from dbt.cli.main import dbtRunner, dbtRunnerResult

# Set the path to the service account key, loaded by Cloud Run from Secret Manager
keyfile_path = '/keys/service-account.json'

# Get the project ID from the service account key
with open(keyfile_path) as f:
    data = json.load(f)
    project_id = data['project_id']

# Set the collection and document name
collection_name = 'dbt-settings'
document_name = 'dbt-settings'

# Authenticate and initialize Firestore
db = firestore.Client.from_service_account_json(keyfile_path)

# Get the document from Firestore
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

# TODO: Validate if the insentric_schema_version is within the allowed range

# Push all available data to the environment variables, which will be used by dbt
for key, value in data.items():
    os.environ['DBT_ENV_' + key.upper()] = str(value)

# Instantiate the logging client
logging_client = logging.Client()
log_name = 'dbt-run'
logger = logging_client.logger(log_name)

# Run the dbt project commands
dbt = dbtRunner()

# Set the arguments for dbt, and run the dbt run commands
cli_args = ["--quiet", "run", "--target", "cloudrun"]
res: dbtRunnerResult = dbt.invoke(cli_args)

# Log the results to the cloud, based on the exit code
if res.success:
    logger.log_text('dbt run completed successfully', severity='INFO')
elif res.exception is None:
    logger.log_text('dbt run completed with warnings', severity='WARNING')
    print(res.result)
    logger.log_text(res.stdout, severity='WARNING')
else:
    logger.log_text('dbt run failed', severity='ERROR')
    print(res.result)
    logger.log_text(res.exception, severity='ERROR')

# Set the arguments for dbt, and run the dbt run commands
cli_args = ["--quiet", "test", "--target", "cloudrun"]
res: dbtRunnerResult = dbt.invoke(cli_args)

# Log the results to the cloud, based on the exit code
if res.success:
    logger.log_text('dbt test completed successfully', severity='INFO')
elif res.exception is None:
    logger.log_text('dbt test completed with warnings', severity='WARNING')
    print(res.result)
    logger.log_text(res.stdout, severity='WARNING')
else:
    logger.log_text('dbt test failed', severity='ERROR')
    print(res.result)
    logger.log_text(res.exception, severity='ERROR')

# TODO: Run the dbt docs commands

logger.log_text('dbt cloud run completed', severity='INFO')

# End of script