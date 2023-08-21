import json
import os
import weaviate
from dotenv import load_dotenv
import requests

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

class_name = "JeopardyQuestion"

class_obj = {
    "class": class_name,
    "vectorizer": "text2vec-openai",
    # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {
            "model": "gpt-3.5-turbo"
        }  # Ensure the `generative-openai` module is used for generative queries
    }
}

# client.schema.create_class(class_obj)

jeopardy_url = 'https://raw.githubusercontent.com/databyjp/wv_demo_uploader/main/weaviate_datasets/data/jeopardy_1k.json'

# resp = requests.get(jeopardy_url)
# data = json.loads(resp.text)  # Load data
#
# with client.batch() as batch:  # Initialize a batch process
#     for i, d in enumerate(data):  # Batch import data
#         print(f"importing question: {i+1}")
#         properties = {
#             "answer": d["Answer"],
#             "question": d["Question"],
#         }
#         batch.add_data_object(
#             data_object=properties,
#             class_name="JeopardyQuestion"
#         )

#
# === Querying ===
#

response1 = (
    client.query
    .get("JeopardyQuestion", ["question", "answer"])
    # .with_additional("vector")
    .with_additional("id")
    .with_near_text({
        "concepts": ["sports, baseball and basketball"],
        "distance": 0.5
    })
    .with_autocut(2)
    .with_limit(10)
    .with_additional(["distance"])
    .do()
)

print(json.dumps(response1, indent=2))

if __name__ == '__main__':
    pass
