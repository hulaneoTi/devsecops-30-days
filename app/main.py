"""Minimal API used as the target of the DevSecOps pipeline."""

from flask import Flask, jsonify, request

app = Flask(__name__)

ITEMS: dict[int, str] = {}


@app.after_request
def security_headers(response):
    # Basic hardening headers. OWASP ZAP checks for these in the DAST stage.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    return response


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/items")
def list_items():
    return jsonify(items=[{"id": i, "name": n} for i, n in ITEMS.items()])


@app.post("/items")
def create_item():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    if not name or len(name) > 100:
        return jsonify(error="name is required (max 100 chars)"), 400
    item_id = len(ITEMS) + 1
    ITEMS[item_id] = name
    return jsonify(id=item_id, name=name), 201
