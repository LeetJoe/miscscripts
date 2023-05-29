
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


# example function for handling exceptions for python lib
def exception_handel():
    try:
      #Make your OpenAI API request here
      response = openai.Completion.create(prompt="Hello world",
                                          model="text-davinci-003")
    except openai.error.APIError as e:
      #Handle API error here, e.g. retry or log
      print(f"OpenAI API returned an API Error: {e}")
      pass
    except openai.error.APIConnectionError as e:
      #Handle connection error here
      print(f"Failed to connect to OpenAI API: {e}")
      pass
    except openai.error.RateLimitError as e:
      #Handle rate limit error (we recommend using exponential backoff)
      print(f"OpenAI API request exceeded rate limit: {e}")
      pass