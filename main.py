import json

import functions_framework
from flask import Request, jsonify
from google.cloud import storage

from src.example.solvers import SomeSolver
from src.models import Input


@functions_framework.http
def apply_some_solver(request: Request):
    content_type = request.headers["content-type"]
    if "application/json" in content_type:
        request_json = request.get_json(silent=True)
    else:
        raise ValueError(f"Unknown content type: {content_type}")
    print(request_json)
    response_data = jsonify(SomeSolver().process(Input.from_dict(request_json)))

    return response_data


@functions_framework.http
def save_result(request: Request):
    content_type = request.headers["content-type"]
    if "application/json" in content_type:
        request_json = request.get_json(silent=True)
    else:
        raise ValueError("Unknown content type: {content_type}")
    print(request_json)
    response_data = json.dumps(request_json["result"])
    bucket_name = request_json["bucket"]
    object_name = request_json["object"]

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    print(f"Saving result to {object_name} in bucket {bucket_name}.")
    blob.upload_from_string(response_data, content_type="application/json")
    print("File saved.")

    return "Done."
