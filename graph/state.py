# graph/state.py
from typing import TypedDict, Any

class MarketingState(TypedDict, total=False):
    cars_tools: list
    emails_tools: list
    cars: Any
    clients: Any
    promotions: list
    text: str
    final_emails: list