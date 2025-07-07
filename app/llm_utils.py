import os
import requests

API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

def call_mistral_featherless(prompt: str, hf_token: str) -> str:
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]