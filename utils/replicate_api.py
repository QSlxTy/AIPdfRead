import base64
import os

import replicate

from src.config import Configuration

REPLICATE_API_TOKEN = Configuration.replicate_token

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN


async def replicate_func(image_path):
    with open(image_path, 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        image = f"data:application/octet-stream;base64,{data}"

        output = await replicate.async_run(
            "abiruyt/text-extract-ocr:a524caeaa23495bc9edc805ab08ab5fe943afd3febed884a4f3747aa32e9cd61",
            input={
                "image": image
            }
        )
        print(output)
        print(output['output'])
        return output['output']
