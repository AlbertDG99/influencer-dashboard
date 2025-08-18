from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AppConfig:
	secret_key: str
	cors_origins: List[str]
	log_level: str
	enable_security_headers: bool
	flask_env: str

	@staticmethod
	def from_env() -> "AppConfig":
		return AppConfig(
			secret_key=os.getenv("SECRET_KEY", "dev-secret"),
			cors_origins=[o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5000").split(",") if o.strip()],
			log_level=os.getenv("LOG_LEVEL", "INFO"),
			enable_security_headers=os.getenv("ENABLE_SECURITY_HEADERS", "true").lower() == "true",
			flask_env=os.getenv("FLASK_ENV", "development"),
		)

	def to_flask_config(self) -> dict:
		return {
			"SECRET_KEY": self.secret_key,
			"ENV": self.flask_env,
			"DEBUG": self.flask_env == "development",
		}

