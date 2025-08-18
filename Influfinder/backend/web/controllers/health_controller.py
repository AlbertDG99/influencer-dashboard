from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, Gauge


health_bp = Blueprint("health_bp", __name__)
_app_up = Gauge("influfinder_app_up", "Application up status")
_app_up.set(1)


@health_bp.get("/health")
def health() -> Any:
	return jsonify({"status": "ok"})


@health_bp.get("/metrics")
def metrics():
	return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
