import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.url_map.strict_slashes = False
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app, resources={r"/*": {"origins": "*"}})

_route_error = None

@app.route("/")
def index():
    return jsonify({
        "service": "TeraBox Standalone API",
        "version": "1.0.0",
        "status": "online",
        "routes_loaded": _route_error is None,
        "endpoints": {
            "terabox": "/terabox?url=TERABOX_URL",
            "terabox_with_pwd": "/terabox?url=TERABOX_URL&pwd=PASSWORD",
        },
    })

@app.route("/health")
def health():
    payload = {"status": "ok" if _route_error is None else "degraded", "routes_loaded": _route_error is None}
    if _route_error:
        payload["route_import_error"] = _route_error
    return jsonify(payload), (200 if _route_error is None else 500)

try:
    from routes.terabox import terabox_bp
    app.register_blueprint(terabox_bp)
except Exception as exc:
    _route_error = f"{type(exc).__name__}: {exc}"
    print("TeraBox route import failed:")
    traceback.print_exc()

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
