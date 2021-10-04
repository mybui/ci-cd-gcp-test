import json

from google.cloud import bigquery

import settings


# use Google Cloud Logging when run on Cloud Run
if settings.LOG == "remote":
    import google.cloud.logging

    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()
else:
    # use standard logging if run locally
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )


class BigQueryClient(object):
    def __init__(self):
        self.client = bigquery.Client()

    def insert(self, table_name, json_file_address):
        try:
            with open(json_file_address) as json_file:
                data = json.load(json_file)

            table_id = f"{settings.GOOGLE_CLOUD_PROJECT}.{settings.GOOGLE_CLOUD_DATASET}.{table_name}"
            job_config_write = bigquery.LoadJobConfig(
                write_disposition=getattr(bigquery.WriteDisposition, "WRITE_TRUNCATE"),
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            )
            job = self.client.load_table_from_json(
                data, table_id, job_config=job_config_write
            )
            job.result()
        except Exception as e:
            logging.error("Error while loading {} table {}".format(table_name, str(e)))
