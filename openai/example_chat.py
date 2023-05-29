# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import openai

from envvar import api_key


# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

def role_playing():
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    return response



resp = role_playing()
for choice in sorted(resp.choices, key=lambda r: r.index):
    # TODO: 按 index 排序。
    print('[', choice.index, ']', choice.message.role, ':', choice.message.content)



# <OpenAIObject chat.completion id=chatcmpl-7LNdMYuPCTEoAbIlITH8glfe10VUd at 0x7fbdb7b04ef0> JSON: {
#   "choices": [
#     {
#       "finish_reason": "stop",
#       "index": 0,
#       "message": {
#         "content": "The 2020 World Series was played at a neutral-site location, Globe Life Field in Arlington, Texas.",
#         "role": "assistant"
#       }
#     }
#   ],
#   "created": 1685330092,
#   "id": "chatcmpl-7LNdMYuPCTEoAbIlITH8glfe10VUd",
#   "model": "gpt-3.5-turbo-0301",
#   "object": "chat.completion",
#   "usage": {
#     "completion_tokens": 22,
#     "prompt_tokens": 57,
#     "total_tokens": 79
#   }
# }


# finish reason: stop是指正常结束，length是指超出了token数量限制；content_filter是指触发了openai的内容过滤机制；null是指回答还在进行中。
# usage 里面显示了这次请求的token cost，prompt tokens是提问里的数量，completion tokens是回答里的数量。

