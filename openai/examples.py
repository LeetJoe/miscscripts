
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


def summarize_for_2nd_grade():
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Summarize this for a second-grade student:\n\nJupiter is the fifth planet from the Sun and the largest in the Solar System. It is a gas giant with a mass one-thousandth that of the Sun, but two-and-a-half times that of all the other planets in the Solar System combined. Jupiter is one of the brightest objects visible to the naked eye in the night sky, and has been known to ancient civilizations since before recorded history. It is named after the Roman god Jupiter.[19] When viewed from Earth, Jupiter can be bright enough for its reflected light to cast visible shadows,[20] and is on average the third-brightest natural object in the night sky after the Moon and Venus.",
      temperature=0.7,
      max_tokens=64,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    return response


def nl_to_code_openaiAPI():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="\"\"\"\nUtil exposes the following:\nutil.openai() -> authenticates & returns the openai module, which has the following functions:\nopenai.Completion.create(\n    prompt=\"<my prompt>\", # The prompt to start completing from\n    max_tokens=123, # The max number of tokens to generate\n    temperature=1.0 # A measure of randomness\n    echo=True, # Whether to return the prompt in addition to the generated completion\n)\n\"\"\"\nimport util\n\"\"\"\nCreate an OpenAI completion starting from the prompt \"Once upon an AI\", no more than 5 tokens. Does not include the prompt.\n\"\"\"\n",
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    return response


def text_to_command():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Convert this text to a programmatic command:\n\nExample: Ask Constance if we need some bread\nOutput: send-msg `find constance` Do we need some bread?\n\nReach out to the ski store and figure out if I can get my skis fixed before I leave on Thursday",
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.2,
        presence_penalty=0.0,
        stop=["\n"]
    )

    return response


# Translates English text into French, Spanish and Japanese.
def english_to_other_lang():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Translate this into 1. French, 2. Spanish and 3. Japanese:\n\nWhat rooms do you have available?\n\n1.",
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response


# Create code to call the Stripe API using natural language.
def nl_to_stripeAPI():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="\"\"\"\nUtil exposes the following:\n\nutil.stripe() -> authenticates & returns the stripe module; usable as stripe.Charge.create etc\n\"\"\"\nimport util\n\"\"\"\nCreate a Stripe token using the users credit card: 5555-4444-3333-2222, expiration date 12 / 28, cvc 521\n\"\"\"",
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    return response


# Translate natural language to SQL queries.
def sql_translate():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\nSELECT",
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
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


