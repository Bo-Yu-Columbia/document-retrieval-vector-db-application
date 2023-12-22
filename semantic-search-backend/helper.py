import os
import requests
import base64

def encode_image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def extract_content(response_json):
    # Check if 'choices' key exists and it has at least one element
    if 'choices' in response_json and response_json['choices']:
        first_choice = response_json['choices'][0]
        # Check if 'message' and 'content' keys exist in the first choice
        if 'message' in first_choice and 'content' in first_choice['message']:
            return first_choice['message']['content']
    return "Content not found or invalid response structure."

def process_image_with_openai(base64_image):
    # OpenAI API Call with the base64 encoded image
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
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
    return extract_content(response.json())  # Use the existing extract_content function
