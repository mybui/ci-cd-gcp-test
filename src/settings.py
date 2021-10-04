import os

PORT = os.environ.get("PORT", 8080)

LOG = os.environ.get("LOG", "remote")

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')
GOOGLE_CLOUD_DATASET = os.environ.get('GOOGLE_CLOUD_DATASET')