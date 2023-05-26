
# imports
import random
import time

# 统计一分钟窗口内的发送情况
rate_acc = {
    'ada': [
        {
            'mt': 8888888888888,   # time in millisecond
            'tnum': 1000    # token number
        },
    ],
    'curie': [
        {
            'mt': 8888888888888,
            'tnum': 1000
        }
    ]
}

# in millisecond, 50s < 60s
acc_window = 55000

# in seconds
wait_interval = 0.2

# overflow wait
overflow_wait_step = [2, 4, 8, 16, 32, 64]

# internal wait
def inter_wait():
    time.sleep(wait_interval)

# overflow wait
def overflow_wait(count):
    if count <= 0:
        return

    if count > len(overflow_wait_step):
        # TODO: log or alert here
        count = len(overflow_wait_step)

    time.sleep(overflow_wait_step[count - 1] + random.randrange(0, 10)/10)






'''

# sample method to avoid exponential #1
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


completion_with_backoff(model="text-davinci-003", prompt="Once upon a time,")



# sample method to avoid exponential #2
import backoff
import openai


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


completions_with_backoff(model="text-davinci-003", prompt="Once upon a time,")



# define a retry decorator
def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 10,
        errors: tuple = (openai.error.RateLimitError,),
):
    """Retry a function with exponential backoff."""

    def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        # Loop until a successful response or max_retries is hit or an exception is raised
        while True:
            try:
                return func(*args, **kwargs)

            # Retry on specific errors
            except errors as e:
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e

    return wrapper


@retry_with_exponential_backoff
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)

'''