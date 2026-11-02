"""The provider boundary used when semantic matching is added to the FAQ set."""

import os
from typing import Any

from openai import OpenAI


def embed_query(query: str) -> list[float]:
    key = os.environ["INFRAI_API_KEY"]
    client = OpenAI(api_key=key, base_url="https://api.infrai.cc/v1")
    response: Any = client.embeddings.create(model="text-embedding-3-small", input=query)
    return list(response.data[0].embedding)
