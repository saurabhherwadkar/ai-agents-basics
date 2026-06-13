"""Describe an image using the OpenAI Vision API."""

from openai import OpenAI

from config import DEFAULT_IMAGE_PATH, MODEL_NAME, OPENAI_API_KEY, VISION_MAX_TOKENS

import base64


def describe_image(image_path: str = DEFAULT_IMAGE_PATH) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=VISION_MAX_TOKENS,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print(describe_image())
