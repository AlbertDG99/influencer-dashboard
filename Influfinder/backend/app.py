from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory, g, request
from flask_cors import CORS
from prometheus_client import Counter

from backend.config import AppConfig
from backend.logging_config import configure_logging
from backend.utils.security import apply_security_headers
from backend.web.errors import register_error_handlers
from backend.web.controllers.influencer_controller import influencer_bp
from backend.web.controllers.export_controller import export_bp
from backend.web.controllers.health_controller import health_bp
from backend.api.docs.swagger import swagger_bp, openapi_json


load_dotenv()

REQUEST_COUNT = Counter("influfinder_http_requests_total", "HTTP requests", ["method", "endpoint", "status"])  # type: ignore
ERROR_COUNT = Counter("influfinder_http_errors_total", "HTTP errors", ["endpoint", "status"])  # type: ignore


def create_app(config: AppConfig | None = None) -> Flask:
	app = Flask(
		__name__,
		static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"),
		static_url_path="/",
	)

	app_config = config or AppConfig.from_env()
	app.config.update(app_config.to_flask_config())

	configure_logging(level=app_config.log_level)
	CORS(app, resources={r"/api/*": {"origins": app_config.cors_origins}})
	apply_security_headers(app, enable=app_config.enable_security_headers)

	@app.before_request
	def _before_request():
		g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

	@app.after_request
	def _after_request(response):
		response.headers["X-Request-ID"] = g.get("request_id", "-")
		status = response.status_code
		endpoint = request.path
		REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status).inc()  # type: ignore
		if status >= 400:
			ERROR_COUNT.labels(endpoint=endpoint, status=status).inc()  # type: ignore
		return response

	app.register_blueprint(influencer_bp, url_prefix="/api/influencers")
	app.register_blueprint(export_bp, url_prefix="/api/export")
	app.register_blueprint(health_bp, url_prefix="/api")
	app.register_blueprint(swagger_bp)

	register_error_handlers(app)

	@app.get("/")
	def index() -> Any:
		return send_from_directory(app.static_folder, "index.html")

	@app.get("/api/openapi.json")
	def get_openapi() -> Any:
		return jsonify(openapi_json(app))

	return app


app = create_app()


if __name__ == "__main__":
	port = int(os.getenv("PORT", "5000"))
	app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
