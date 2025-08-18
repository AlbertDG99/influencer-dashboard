from __future__ import annotations

import logging
from typing import Optional

from pythonjsonlogger import jsonlogger


def configure_logging(level: str = "INFO") -> None:
	logger = logging.getLogger()
	logger.setLevel(level)

	if logger.handlers:
		return

	handler: logging.Handler = logging.StreamHandler()
	formatter = jsonlogger.JsonFormatter(
		"%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d"
	)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

