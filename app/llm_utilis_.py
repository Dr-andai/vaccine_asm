# llm_utils.py

import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="novita",
    api_key=os.environ.get("HF_TOKEN")
)

def ask_mistral(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling model: {str(e)}"
