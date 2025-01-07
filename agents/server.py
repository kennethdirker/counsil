from pathlib import Path
from typing import Any
import time

from transformers import pipeline, DistilBertForQuestionAnswering, DistilBertTokenizer




def init_counselors():
    """
    Loads the profiles that are used to initialize swarm agents.

    Returns
        List of maps containing the $name and $system_prompt for each counselor.  
    """
    start = time.time()
    print("Loading counselor profiles...")
    users = [
        {"name": "Karen", "system_prompt": "Your name is Karen and you work as a location manager at McDonalds."},
        # {"name": "Bob", "system_prompt": f"Your name is Bob. When asked a question you state your name and write the next number. "},
        # {"name": "Heinrich", "system_prompt": f"Your name is Heinrich. When asked a question you state your name and write the next number. "},
    ]
    print(f"{len(users)} profiles loaded in {time.time() - start:.2f} seconds.")
    return users


def init_model():
    start = time.time()
    model_path = Path("model_bin")
    model_path /= "TinyLlama-1.1B-Chat-v1.0"
    print(f"Loading model and tokenizer from {model_path}")
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print(f"Model and tokenizer loaded in {time.time() - start:.2f} seconds.")
    return model, tokenizer


def init_agents(
        users: list[dict[str, str]],
        model: Any,
        tokenizer
    ) -> list[CounselAgent]:
    """
    
    """
    start = time.time()
    print("Loading agents...")
    agents = []
    for user in users:
        agents.append(CounselAgent(
            user["name"],
            model,
            tokenizer,
            user["system_prompt"],
            # path
        ))
    print(f"{len(agents)} agents loaded in {time.time() - start:.2f} seconds.")
    return agents


def main():
    """"""
    # Initialize a pre-trained pipeline from local storage
    model, tokenizer = init_model()

    # Initialize counselor profiles
    counselors = init_counselors()

    # Initialize an agent for each counsil member.
    agents = init_agents(counselors, model, tokenizer)

    # Run something 
    print("Starting loop")
    loop_start = time.time()
    n = len(agents)
    for i in range(1):
        start = time.time()
        agent = agents[i % n]
        output = agent.run("What are your name and profession?")
        print("\t", output)
        print(f"Iteration {i}: {time.time() - start:.2f} seconds.")
    print(f"Loop ended in {time.time() - loop_start:.2f} seconds.")

if __name__ == "__main__":
    main()