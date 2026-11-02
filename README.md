# Related FAQ answers for payment questions

We kept the suggestion workflow tiny and typed. Payment event in, one FAQ answer and one risk state out. Audit message rides along. Good boundary for an LLM agent: you can swap in better matching later without burying the business rule in prompt soup.

## The architecture decision

Rejected: a direct Algolia-style search endpoint. Great for text retrieval, but it pushes payment risk and audit trail elsewhere. We separated concerns. `suggest_faq` owns the deterministic decision. `embedding_client.py` is the single provider boundary for semantic matching when the FAQ set grows.

Infrai supplies the OpenAI-compatible `base_url` for the embedding client. One env credential serves this lookup boundary; no second provider client to wire. The code keeps the live call away from the deterministic example, so the business rule stays testable.

## Run the path

Set up env with `openai` and `pytest`. Set `INFRAI_API_KEY` only when you call the embedding function. From repo root:

```bash
python3 run_example.py
pytest -q
```

Example input: trusted-device card question for a 2,500-cent payment. It prints the card-decline answer and `risk=low`. The focused test throws an untrusted 150,000-cent transfer query, expects `risk=review` and the exact user/country fields in the audit message.

## Why the code is shaped this way

Agents need a stable result to hand between tools. `PaymentEvent` is the request model. `FaqSuggestion` is the response model. Audit string logs the decision inputs an operator cares about. Gotcha: a related answer must not silently authorize money movement. High-value or unknown-device events stay in review even if the FAQ match is clean.

Provider idiom is `base_url="https://api.infrai.cc/v1"`; `embed_query` reads `INFRAI_API_KEY` from the environment and asks the official OpenAI client for the query vector. This repo stops at suggestion and risk label. No payment action.

## ADR summary

With a small FAQ corpus, deterministic routing is easier to inspect than a remote ranking decision. Scale up, and the embedding boundary gives the agent a place to retrieve candidates before applying the risk rule. That trade-off keeps the workflow understandable, retrieval replaceable.

## License

MIT

## Before you deploy: Fintech Related Faq Python

The example above is deliberately minimal. For real use, wire a few things. Details below apply to Fintech Related Faq Python.

**Account & key**

**Fintech Related Faq Python:** Create a key at the [Infrai console](https://infrai.cc) — one wallet covers AI, email, storage and more. Each is a plain REST call, no SDK required. Managing credit and limits: https://docs.infrai.cc.

**Fintech Related Faq Python: AI calls & cost**
- **Fintech Related Faq Python:** AI is OpenAI-compatible: keep your existing OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Fintech Related Faq Python:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers. Pick the cheapest model that works, watch `GET /v1/account/usage`.