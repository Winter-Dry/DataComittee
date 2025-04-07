import os, sys
import json
import requests


class LLM:
    def __init__(self):
        pass

    def __call__(self, input):
        pass


class OpenAI_like_api_LLM(LLM):

    def __init__(self, url=None, model_name="auto"):
        super().__init__()
        self.original_url = url
        self.url = "{}/v1/chat/completions".format(url)
        if model_name == 'auto':
            self._auto_get_model_name()
        else:
            self.model_name = model_name

        print('using url:', self.url)

    def _auto_get_model_name(self):
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.get('{}/v1/models'.format(self.original_url), headers=headers)
        self.model_name = response.json()['data'][0]['id']

    def __call__(
            self, prompt: str,
            model_name: str = None,
            temperature: float = 0.7,
            max_tokens: int = 10000,
            stream=False,
    ):
        # print(prompt)
        if model_name is None:
            model_name = self.model_name

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        response = requests.post(self.url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response = response.json()['choices'][0]['message']['content']
        else:
            print(f"Request failed with status code {response.status_code}, {response.json()}")
        # print(response)
        return response


if __name__ == "__main__":
    llm = OpenAI_like_api_LLM('http://localhost:8000', model_name='auto')

    print(llm('1+1等于几'))