from __future__ import annotations

from typing import Any, Dict, Optional

import requests


class InstagramClient:
    def __init__(self, access_token: Optional[str]) -> None:
        self._access_token = access_token

    def get(self, path: str, params: Optional[dict] = None) -> Dict[str, Any]:
        # Placeholder for real calls
        return {"data": []}

