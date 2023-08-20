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

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-openai",
    # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-openai": {},
        "generative-openai": {}  # Ensure the `generative-openai` module is used for generative queries
    }
}

# client.schema.create_class(class_obj)


# resp = requests.get('https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
# data = json.loads(resp.text)  # Load data

# with client.batch() as batch:  # Initialize a batch process
#     for i, d in enumerate(data):  # Batch import data
#         print(f"importing question: {i+1}")
#         properties = {
#             "answer": d["Answer"],
#             "question": d["Question"],
#             "category": d["Category"],
#         }
#         batch.add_data_object(
#             data_object=properties,
#             class_name="Question"
#         )

#
# === Querying ===
#

# response1 = (
#     client.query
#     .get("Question", ["question", "answer", "category"])
#     .with_additional("id")
#     .with_near_text({"concepts": ["DNA and RNA"]})
#     .with_limit(2)
#     .do()
# )

response1 = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_additional("id")
    .with_near_object({"id": "9b37457f-cc4f-4dff-a2fd-d242a53dd269"})
    .with_limit(2)
    .do()
)

# response2 = (
#     client.query
#     .get("Question", ["question", "answer", "category"])
#     .with_near_text({"concepts": ["biology"]})
#     .with_where({
#         "path": ["category"],
#         "operator": "Equal",
#         "valueText": "ANIMALS"
#     })
#     .with_limit(2)
#     .do()
# )

# response = (
#     client.query
#     .get("Question", ["question", "answer", "category"])
#     .with_near_text({"concepts": ["biology"]})
#     .with_generate(single_prompt="{answer}. continue...  ")
#     .with_limit(2)
#     .do()
# )

# response = (
#     client.query
#     .get("Question", ["question", "answer", "category"])
#     .with_near_text({"concepts": ["biology"]})
#     .with_generate(grouped_task="Write a tweet with emojis about these facts.")
#     .with_limit(2)
#     .do()
# )


print(json.dumps(response1, indent=2))


if __name__ == '__main__':
    pass
