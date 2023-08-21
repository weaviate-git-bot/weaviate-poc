import json
import os
import weaviate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get values from environment variables
WEAVIATE_URL = os.environ.get('WEAVIATE_URL')
WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Check if values are set
if not WEAVIATE_URL or not WEAVIATE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Both WEAVIATE_URL and WEAVIATE_API_KEY must be set in environment variables.")

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
    additional_headers={
        "X-OpenAI-Api-Key": OPENAI_API_KEY
    }
)

ret = client.schema.get()
print(ret)

jeopardy_url = 'https://raw.githubusercontent.com/databyjp/wv_demo_uploader/main/weaviate_datasets/data/jeopardy_1k.json'

#
# === Querying ===
#

# An alpha of 1 is for a pure vector search and 0 is for a pure keyword search.
response1 = (
    client.query
    .get("JeopardyQuestion", ["question", "answer"])
    .with_hybrid(
        query="food",
        properties=["question^2", "answer"],
        alpha=0.2,  # 0.75
    )
    .with_additional(["score", "explainScore", "distance"])
    .with_autocut(2)

    .do()
)

print(json.dumps(response1, indent=2))

if __name__ == '__main__':
    pass
