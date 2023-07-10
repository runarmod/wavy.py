import io

from flask import Flask, request, send_file
from flask_cors import CORS

from wavy import Wavy

app = Flask(__name__)
CORS(app)


def create_wavy() -> Wavy:
    wave_args = {
        "width",
        "height",
        "color",
        "start",
        "points",
        "wonkyness",
        "resolution",
        "format",
    }
    params = normalize_params(wave_args)

    return Wavy(**params)  # type: ignore


def normalized_param(key: str, value):
    if key in ("start", "wonkyness", "start_y", "end_y"):
        return float(value[0])
    return (
        int(value[0]) if key in ("width", "height", "points", "layers", "resolution") else value[0]
    )


def normalize_params(params):
    query_params = request.args.to_dict(flat=False)
    return {k: normalized_param(k, v) for k, v in query_params.items() if k in params}


@app.route("/")
def index():
    return "Hello, World!\nCheck https://github.com/runarmod/wavy for more info.\n"


@app.route("/api/wave")
def wave():
    wavy = create_wavy()

    if wavy.format == "svg":
        return send_file(
            io.BytesIO(bytes(str(wavy.generate_wave()), encoding="utf-8")), mimetype="image/svg+xml"
        )
    return wavy.generate_wave()


@app.route("/api/waves")
def waves():
    wavy = create_wavy()
    wavy.set_format("json")

    options_args = {"layers", "start_color", "end_color", "start_y", "end_y"}
    params = normalize_params(options_args)

    return wavy.generate_waves(**params)  # type: ignore
