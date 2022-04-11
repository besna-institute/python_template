from flask import Request, jsonify

from src.example.solvers import SomeSolver


def apply_some_solver(request: Request):
    # content_type = request.headers["content-type"]
    # if "application/json" in content_type:
    #     request_json = request.get_json(silent=True)
    # else:
    #     raise ValueError("Unknown content type: {}".format(content_type))
    # print(request_json)
    # response_data = jsonify(SomeSolver().process(request_json))

    # return response_data
    return "hello"


def hello_world(request):
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
