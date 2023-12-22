from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
print(openai_api_key)
import base64
import requests


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


# Path to your image
image_path = r"/Users/yubo/Desktop/test3.jpg"
# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "tell me what is in this picture using sentence as concise as possible"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())


def extract_content(response_json):
    # Check if 'choices' key exists and it has at least one element
    if 'choices' in response_json and response_json['choices']:
        first_choice = response_json['choices'][0]
        # Check if 'message' and 'content' keys exist in the first choice
        if 'message' in first_choice and 'content' in first_choice['message']:
            return first_choice['message']['content']
    return "Content not found or invalid response structure."


content = extract_content(response.json())
print(content)
