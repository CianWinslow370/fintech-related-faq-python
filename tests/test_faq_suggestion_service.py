from src.faq_suggestion_service import PaymentEvent, suggest_faq


def test_high_value_untrusted_payment_requires_review_and_keeps_answer_auditable():
    result = suggest_faq(PaymentEvent("u-7", "Where is my transfer?", 150_000, "US", False))
    assert result.question == "Where is my transfer?"
    assert result.risk == "review"
    assert result.audit_message == "faq_suggestion user=u-7 country=US risk=review"
