import json

from flask import Flask

import bq_client
import settings

print("Logging is currently {0}".format(settings.LOG))

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

app = Flask(__name__)


@app.route("/")
def sync():
    logging.debug("Execution started")

    client = bq_client.BigQueryClient()
    client.insert("Colors", "data/colors.json")

    logging.debug("Execution ended")

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(settings.PORT))
