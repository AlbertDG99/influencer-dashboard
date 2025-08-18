from __future__ import annotations

from typing import Any, Dict, List


class ScrapingService:
    """Abstraction over HTML scraping to collect influencer-like data.

    Note:
        In production, comply with ToS and legal requirements.
    """

    def search_hashtag(self, hashtag: str) -> List[Dict[str, Any]]:
        """Search public posts for a hashtag.

        Args:
            hashtag: Hashtag without leading '#'.

        Returns:
            A list of simplified post/user dicts.
        """
        return []
