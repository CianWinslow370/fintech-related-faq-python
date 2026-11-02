"""A small, typed workflow for risk-aware FAQ suggestions."""

from dataclasses import dataclass
from typing import Literal


Risk = Literal["low", "review", "blocked"]


@dataclass(frozen=True)
class PaymentEvent:
    user_id: str
    query: str
    amount_cents: int
    country: str
    trusted_device: bool


@dataclass(frozen=True)
class FaqSuggestion:
    question: str
    answer: str
    risk: Risk
    audit_message: str


FAQS = (
    ("Where is my transfer?", "Transfers usually arrive after the receiving bank accepts them."),
    ("Why was my card payment declined?", "Check the available balance and confirm the card details."),
    ("How do I verify my identity?", "Open verification in settings and follow the identity checks."),
)


def suggest_faq(event: PaymentEvent) -> FaqSuggestion:
    """Return a concrete answer while making a risk-sensitive action explicit."""
    text = event.query.lower()
    if event.amount_cents >= 100_000 or not event.trusted_device:
        risk: Risk = "review"
    else:
        risk = "low"
    if "declin" in text or "card" in text:
        question, answer = FAQS[1]
    elif "verify" in text or "identity" in text:
        question, answer = FAQS[2]
    else:
        question, answer = FAQS[0]
    audit = f"faq_suggestion user={event.user_id} country={event.country} risk={risk}"
    return FaqSuggestion(question, answer, risk, audit)
