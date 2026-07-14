"""REST API server for remote integrity checks."""
from flask import Flask, jsonify, request
from .checker import IntegrityChecker

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "service": "integrity-checker API",
        "version": "0.1.0",
        "endpoints": [
            "GET /check/<device>",
            "POST /batch",
            "GET /health"
        ]
    })

@app.route("/check/<path:device>")
def check_device(device):
    """Check integrity of a device."""
    # Ensure device has port
    if ":" not in device:
        device = f"{device}:5555"
    try:
        checker = IntegrityChecker(device)
        result = checker.run_check()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/batch", methods=["POST"])
def batch_check():
    """Batch check multiple devices."""
    data = request.json
    devices = data.get("devices", [])
    results = []
    for device in devices:
        try:
            checker = IntegrityChecker(device)
            results.append(checker.run_check())
        except Exception as e:
            results.append({"device": device, "error": str(e)})
    return jsonify(results)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})
