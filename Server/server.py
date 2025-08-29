from flask import Flask, request
import datetime
import logging
from logging.handlers import RotatingFileHandler
import json

app = Flask(__name__)


log_handler = RotatingFileHandler(
    "data_received.log",
    maxBytes=5 * 1024 * 1024,  
    backupCount=5,  
    encoding="utf-8"
)
log_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(message)s")
log_handler.setFormatter(formatter)

app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json
    pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
    app.logger.info("\n=======================\n%s\n=======================\n", pretty_json)

    
    return {"status": "OK"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)
