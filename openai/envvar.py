api_key=''

# other limit refer to the table in https://platform.openai.com/account/rate-limits
rate_limit = {
    'gpt-3.5-turbo' : [3, 40000],
    'gpt-3.5-turbo-0301' : [3, 40000],

    'ada': [60, 150000],
    'curie': [60, 150000],
    'davinci': [60, 150000],

    'code-davinci-edit-001': [20, 150000],

    'text-davinci-001': [60, 150000],
    'text-davinci-002': [60, 150000],
    'text-davinci-003': [60, 150000],
    'text-davinci-edit-001': [20, 150000],

    'DALL·E 2': [3, 5],
    'whisper-1': [50, 150000]
}

# limit if not defined in rate_limit
default_limit = [60, 150000]


