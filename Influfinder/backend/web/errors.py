from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Tuple

from flask import Flask, jsonify


class AppError(Exception):
	status_code: int = 400
	code: str = "app_error"

	def __init__(self, message: str, *, status_code: int | None = None, code: str | None = None) -> None:
		super().__init__(message)
		if status_code is not None:
			self.status_code = status_code
		if code is not None:
			self.code = code
		self.message = message


class NotFoundError(AppError):
	status_code = 404
	code = "not_found"


class ValidationError(AppError):
	status_code = 422
	code = "validation_error"


class ExternalServiceError(AppError):
	status_code = 502
	code = "external_service_error"


@dataclass
class ErrorResponse:
	message: str
	code: str
	status: int

	def to_dict(self) -> Dict[str, Any]:
		return {"error": {"message": self.message, "code": self.code}, "status": self.status}


def register_error_handlers(app: Flask) -> None:
	@app.errorhandler(AppError)
	def handle_app_error(error: AppError) -> Tuple[Any, int]:
		resp = ErrorResponse(message=str(error), code=error.code, status=error.status_code)
		return jsonify(resp.to_dict()), error.status_code

	@app.errorhandler(404)
	def handle_404(_: Any) -> Tuple[Any, int]:
		resp = ErrorResponse(message="Recurso no encontrado", code="not_found", status=404)
		return jsonify(resp.to_dict()), 404

	@app.errorhandler(500)
	def handle_500(error: Any) -> Tuple[Any, int]:
		resp = ErrorResponse(message="Error interno", code="internal_error", status=500)
		return jsonify(resp.to_dict()), 500

