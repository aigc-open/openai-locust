from locust import HttpUser, task, between, TaskSet, tag
import random
import os
import string
from loguru import logger

longest_input = ''.join(random.choices(
    string.ascii_letters + string.digits, k=2048))

# 生成固定长度的随机字符串


def random_string(length):
    if not os.environ.get('RANDOM_STRING'):
        return longest_input[:length]
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def chat_data(input_len=128, output_len=128, model="codechat"):
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": random_string(input_len)}
        ],
        "stream": False,
        "max_tokens": output_len,
        "temperature": 0.0
    }


def generation_data(input_len=128, output_len=128, model="codebase"):
    return {
        "model": model,
        "prompt": random_string(input_len),
        "max_tokens": output_len,
        "temperature": 0.0
    }


class Config:
    input_lens = random.choice([int(i)
                                for i in os.environ.get('INPUT_LENS', '1').split(',')])
    output_lens = random.choice([int(i)
                                 for i in os.environ.get('OUTPUT_LENS', '1').split(',')])
    model = os.environ.get('model', 'codechat')
    headers = {
        "Authorization": os.environ.get("API_KEY", "")
    }


class QuickstartUser(HttpUser):

    @tag('chat_completions')
    @task
    def chat(self):
        self.client.post("/v1/chat/completions",
                         json=chat_data(input_len=input_len, output_len=output_len, model=Config.model), headers=Config.headers)

    @tag('completions')
    @task
    def base(self):
        self.client.post("/v1/completions",
                         json=generation_data(input_len=Config.input_len, output_len=Config.output_len, model=Config.model), headers=Config.headers)
