from src.faq_suggestion_service import PaymentEvent, suggest_faq


def main() -> None:
    event = PaymentEvent(
        user_id="user-42",
        query="Why was my card payment declined?",
        amount_cents=2500,
        country="GB",
        trusted_device=True,
    )
    result = suggest_faq(event)
    print(result.question)
    print(result.answer)
    print(result.audit_message)


if __name__ == "__main__":
    main()
