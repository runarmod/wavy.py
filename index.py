import io

from flask import Flask, request, send_file
from flask_cors import CORS

from wavy import Wavy

app = Flask(__name__)
CORS(app)


def normalized_param(key, value):
    if len(value) > 1:
        return set(value)
    if key in ("start", "wonkyness", "start_y", "end_y"):
        return float(value[0])
    return (
        int(value[0]) if key in ("width", "height", "points", "layers", "resolution") else value[0]
    )


def create_wavy():
    wave_args = {
        "width",
        "height",
        "color",
        "start",
        "points",
        "wonkyness",
        "resolution",
        "only_include",
    }
    params = normalize_params(wave_args)

    return Wavy(**params)


def normalize_params(params):
    query_params = request.args.to_dict(flat=False)
    return {k: normalized_param(k, v) for k, v in query_params.items() if k in params}


@app.route("/")
def index():
    return "Hello, World!\nCheck https://github.com/runarmod/wavy for more info.\n"


@app.route("/api/wave")
def wave():
    wavy = create_wavy()

    return send_file(
        io.BytesIO(bytes(wavy.generate_wave(), encoding="utf-8")), mimetype="image/svg+xml"
    )


@app.route("/api/waves")
def waves():
    wavy = create_wavy()

    options_args = {"layers", "start_color", "end_color", "start_y", "end_y"}
    params = normalize_params(options_args)

    return wavy.generate_waves(**params)
