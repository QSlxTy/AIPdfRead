import ast
import base64

from openai import OpenAI

from src.config import Tokens
from utils.prompts import prompt_user, prompt_system

GPT_API_KEY = Tokens.openai
client = OpenAI(
    api_key=GPT_API_KEY)


async def gpt_get_photo(photo):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(photo)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system",
                   "content": prompt_system},
                  {
                      "role": "user",
                      "content": [
                          {"type": "text", "text": prompt_user},
                          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

                      ],
                  },
                  ],
        temperature=0
    )
    print(response.choices[0].message.content)
    return ast.literal_eval(response.choices[0].message.content.replace('```', ''))
