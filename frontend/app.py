import os
import base64
import flask
import requests
from typing import Union


backend_host = os.environ['APP_BACKEND_HOST']
backend_port = os.environ['APP_BACKEND_PORT']
app = flask.Flask(__name__, template_folder='templates/')


def infer_model(image: bytes) -> Union[bytes, None]:
    request = {
            'image_data': base64.b64encode(image).decode(),
        }

    url = f'http://{backend_host}:{backend_port}/process'
    resp = requests.post(url, json=request)

    if resp.status_code != 200:
        return None

    data = resp.json()
    model_bytes = data.get('model', None)

    if model_bytes is None:
        return None

    model_bytes = base64.b64decode(model_bytes)
    return model_bytes


@app.route('/', methods=('GET', 'POST'))
def process():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')

    if flask.request.method == 'POST':
        file = flask.request.files.get('image', None)

        if file is None:
            return flask.render_template('index.html')

        data = file.read()
        model = infer_model(data)

        response = flask.make_response(model)
        response.headers.set('Content-Type', 'application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment', filename='model.glb')
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)

