"""Describe an image using the OpenAI Vision API."""

# Import the OpenAI client library
from openai import OpenAI

# Import vision-related settings from project config
from config import DEFAULT_IMAGE_PATH, MODEL_NAME, OPENAI_API_KEY, VISION_MAX_TOKENS

# Import base64 for encoding the image file to a data URI
import base64


# Define a function that sends an image to the vision model and returns a description
def describe_image(image_path: str = DEFAULT_IMAGE_PATH) -> str:

    # Create an authenticated OpenAI client instance
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Read the image file and encode it as a base64 string
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")

    # Send the image to the chat completions API with a text prompt
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

    # Return the text content from the model's first response choice
    return response.choices[0].message.content


# Run the function directly when this script is executed
if __name__ == "__main__":
    print(describe_image())
