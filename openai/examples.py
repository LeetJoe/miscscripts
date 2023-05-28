
import os
import openai
from envvar import api_key


# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def list_models():
    openai.organization = "org-loRuQjfKhAJ6qMTVUKViM89L"
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.Model.list()


def get_embeddings(doc):
    """
    :param doc: text string or list of text string
    :return:
    <OpenAIObject list at 0x7ff40530d670> JSON: {
        "data": [
            {
                "embedding": [
                    ...   # length 1536 no matter what doc is
                ],
                "index": 0,
                "object": "embedding"
            }
        ],
        "model": "text-embedding-ada-002-v2",
        "object": "list",
        "usage": {
            "prompt_tokens": 9,
            "total_tokens": 9
        }
    }
    """

    response = openai.Embedding.create(
      input=doc,
      model="text-embedding-ada-002"
    )

    return response





resp = get_embeddings('to be or not to be')

print(resp.data)
