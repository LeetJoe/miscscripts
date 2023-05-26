
import openai
from .envvar_online import api_key


# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def qa():
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\n"]
    )

    return response


def grammer_correction():
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Correct this to standard English:\n\nShe no went to the market.",
      temperature=0,
      max_tokens=60,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    return response



response = qa()

oaobj = response.choices[0]

print(oaobj.text.strip())



def batch_test():
    num_stories = 10
    prompts = ["Once upon a time,"] * num_stories

    # batched example, with 10 story completions per request
    response = openai.Completion.create(
        model="curie",
        prompt=prompts,
        max_tokens=20,
    )

    # match completions to prompts by index
    stories = [""] * len(prompts)
    for choice in response.choices:
        stories[choice.index] = prompts[choice.index] + choice.text

    # print stories
    for story in stories:
        print(story)


# mail.com secret key : wWKno-opXpE-dzcNp-EMArH
'''
response:

<OpenAIObject text_completion id=cmpl-7KL9fZFp7KKi7CgLaYJUGpuS0utsY at 0x7fe147e83100> JSON: {
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": " The Valley of Kings is located in Luxor, Egypt."
    }
  ],
  "created": 1685082235,
  "id": "cmpl-7KL9fZFp7KKi7CgLaYJUGpuS0utsY",
  "model": "text-davinci-003",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 12,
    "prompt_tokens": 233,
    "total_tokens": 245
  }
}


'''


