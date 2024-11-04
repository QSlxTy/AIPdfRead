import ast
import base64
import json

from openai import OpenAI

from src.config import Tokens
from utils.prompts import prompt_user, prompt_system

GPT_API_KEY = Tokens.openai
client = OpenAI(
    api_key=GPT_API_KEY)


async def gpt_get_photo(photo_path, replicate_response):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(photo_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system",
                   "content": prompt_system},
                  {
                      "role": "user",
                      "content": [
                          {"type": "text", "text": prompt_user + replicate_response},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

                      ],
                  },
                  ],
        temperature=0
    )

    async def transform_input(input_string):
        # Преобразуем строку в объект Python
        print(input_string)
        print(type(input_string))
        try:
            data = json.loads(input_string)
        except json.JSONDecodeError:
            raise ValueError("Некорректный формат JSON")

        # Проверяем, является ли data списком
        if isinstance(data, list):
            # Если список содержит более одного элемента
            if len(data) > 1:
                return data  # Возвращаем как есть
            else:
                return [data[0]]  # Возвращаем как список с одним элементом
        else:
            raise ValueError("Ожидался список объектов JSON")
    return await transform_input(response.choices[0].message.content.replace('`', '').replace('json', ''))
