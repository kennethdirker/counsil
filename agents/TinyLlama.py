from pathlib import Path

# External libs
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

path = Path("model_bin")
path /= "TinyLlama-1.1B-Chat-v1.0"
model = AutoModelForCausalLM.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
pipe = pipeline(
    "text-generation", 
    model = model, 
    tokenizer = tokenizer,
    torch_dtype = torch.bfloat16, 
    device_map = "auto"
)
# pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")

# We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
messages = [
    {
        "role": "system",
        "content": "Your name is Karen",
    },
    {"role": "user", "content": "What is your name?"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])