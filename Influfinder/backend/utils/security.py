from __future__ import annotations

from flask import Flask


DEFAULT_CSP = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'"


def apply_security_headers(app: Flask, *, enable: bool = True) -> None:
	if not enable:
		return

	@app.after_request
	def set_headers(response):
		response.headers.setdefault("Content-Security-Policy", DEFAULT_CSP)
		response.headers.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
		response.headers.setdefault("X-Content-Type-Options", "nosniff")
		response.headers.setdefault("X-Frame-Options", "DENY")
		response.headers.setdefault("Referrer-Policy", "no-referrer-when-downgrade")
		response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
		return response

