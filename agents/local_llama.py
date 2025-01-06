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
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
    {
        "role": "user", "content": "How many helicopters can a human eat in one sitting?"
    },
]

prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
print(outputs[0]["generated_text"])


def load_system(path: Path):
    """ 
    Load a model and tokenizer from storage and use initialize a chat pipeline.
    
    Args:
        path: Path to the directory holding model information.

    Returns:
        Pipeline to chat with.
    """
    model = AutoModelForCausalLM.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)
    pipe = pipeline(
        "text-generation", 
        model = model, 
        tokenizer = tokenizer,
        torch_dtype = torch.bfloat16, 
        device_map = "auto"
    )
    return pipe


def load_users() -> list[str]:
    """
    Return a list of usernames for the counsil.
    """
    names = ["karen", "Darren", "Aaron"]
    return names


# def init_log(users: list[str]) -> dict[str, list[dict[str, str]]]:
#     log = {}
#     for user in users:
#         log[user] = []
#     return log


def set_behaviour():
    ...


def get_response(pipe, message_log):
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])


def main():
    print("Loading TinyLlama.")
    path = Path("model_bin")
    path /= "TinyLlama-1.1B-Chat-v1.0"
    pipe = load_system(path)
    users = load_users()
    message_log = []    # list[{"message_id":, "user": ,"role":, "content"}]
    user_idx = 0
    current_user = users[0]
    num_users = len(users)

    i = 0
    while i < 26:
        text = f"what is the {i}e letter of the alphabet?"
        response = get_response(current_user, text, message_log)
        print(current_user, ":", response)

        # Cycle users
        user_idx = (user_idx + 1) % num_users
        current_user = users[user_idx]
        i += 1
        

if __name__ == "__main__":
    main()