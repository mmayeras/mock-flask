import json
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def inspect_request(path):
    """
    This endpoint captures all incoming requests and returns detailed information
    about the request, including method, URL, headers, query parameters, and body.
    """
    request_info = {
        "method": request.method,
        "path": f"/{path}",
        "full_url": request.url,
        "headers": dict(request.headers),
        "query_parameters": request.args.to_dict(),
        "form_data": request.form.to_dict(),
        "json_data": {},
        "raw_body": request.get_data(as_text=True)
    }

    if request.is_json:
        try:
            request_info["json_data"] = request.get_json()
        except Exception as e:
            request_info["json_data_parse_error"] = str(e)
            request_info["json_data"] = None

    return jsonify(request_info), 200

@app.route('/return_code/<int:status_code>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'])
def return_custom_status_code(status_code):
    """
    This endpoint returns a specific HTTP status code passed in the URL.
    For example, accessing /return_code/404 will return a 404 Not Found response.
    """
    if not (100 <= status_code <= 599):
        abort(400, description=f"Invalid HTTP status code: {status_code}. Please provide a code between 100 and 599.")

    return f"Returning HTTP status code: {status_code}", status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

