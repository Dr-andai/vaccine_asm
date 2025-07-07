from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer once
model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

def ask_mistral(prompt: str) -> str:
    conversation = [{"role": "user", "content": prompt}]

    inputs = tokenizer.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Strip prompt from response (only return model answer)
    return response.split("user")[1].split("assistant")[-1].strip()
