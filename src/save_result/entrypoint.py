import json

import functions_framework  # type: ignore
from flask.wrappers import Request, Response
from google.cloud.storage import Client  # type: ignore


@functions_framework.http  # type: ignore
def save_result(request: Request) -> Response:
    if (request_body := request.get_json()) is None:
        raise ValueError("Invalid JSON.")
    print(request_body)
    response_data = json.dumps(request_body["result"])
    bucket_name = request_body["bucket"]
    object_name = request_body["object"]

    storage_client = Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    print(f"Saving result to {object_name} in bucket {bucket_name}.")
    blob.upload_from_string(response_data, content_type="application/json")
    print("File saved.")

    return Response(response="", status=201)
