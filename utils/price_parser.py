import re
from decimal import Decimal, InvalidOperation
from typing import Optional

class PriceParser:
    """Utility for converting price text like '$12.99', 'ILS 120', 'US $19.50' into Decimal."""

    @staticmethod
    def parse_price(price_text: str) -> Optional[Decimal]:
        if not price_text:
            return None

        cleaned = price_text.replace(",", "")
        matches = re.findall(r"\d+(?:\.\d{1,2})?", cleaned)
        if not matches:
            return None

        try:
            return Decimal(matches[0])
        except InvalidOperation:
            return None
