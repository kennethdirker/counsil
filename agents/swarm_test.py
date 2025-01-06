from pathlib import Path
from typing import Any
import time

import torch
from swarms import Agent as SwarmsAgent
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer


# Counselor Agent
class CounselAgent(SwarmsAgent):
    """
    
    """
    def __init__(
            self, 
            agent_name: str, 
            pipeline: Any,
            system_prompt: str, 
            # path: Path, 
            *args, **kwargs
        ):
        super().__init__(
            agent_name = agent_name, 
            system_prompt = system_prompt, 
            # llm = model,
            *args, 
            **kwargs
        )
        self.pipeline = pipeline

        # # Initialize a pre-trained pipeline from local storage
        # model = AutoModelForCausalLM.from_pretrained(path)
        # tokenizer = AutoTokenizer.from_pretrained(path)
        # self.pipeline = pipeline(
        #     "text-generation", 
        #     model = model, 
        #     tokenizer = tokenizer,
        #     torch_dtype = torch.bfloat16, 
        #     device_map = "auto"
        # )
        # self.pipeline = pipeline("text-generation", model=model_name)



    def run(self, task: str) -> str:
        """ Generate text based on the task input. """
        result = self.pipeline(task, max_length=100)
        # result = self.llm(task, max_length=100)
        return result[0]["generated_text"]



def init_counselors():
    """
    Loads the profiles that are used to initialize swarm agents.

    Returns
        List of maps containing the $name and $system_prompt for each counselor.  
    """
    start = time.time()
    print("Loading counselor profiles...")
    users = [
        {"name": "Karen", "system_prompt": f"Your name is Karen."},
        # {"name": "Bob", "system_prompt": f"Your name is Bob. When asked a question you state your name and write the next number. "},
        # {"name": "Heinrich", "system_prompt": f"Your name is Heinrich. When asked a question you state your name and write the next number. "},
    ]
    print(f"{len(users)} profiles loaded in {time.time() - start:.2f} seconds.")
    return users


def init_pipeline():
    start = time.time()
    model_path = Path("model_bin")
    model_path /= "TinyLlama-1.1B-Chat-v1.0"
    print(f"Loading pipeline with {model_path}")
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    pipe = pipeline(
        "text-generation", 
        model = model, 
        tokenizer = tokenizer,
        torch_dtype = torch.bfloat16, 
        device_map = "auto"
    )
    print(f"Pipeline loaded in {time.time() - start:.2f} seconds.")
    return pipe


def init_agents(
        users: list[dict[str, str]],
        pipeline: Any
        # path: Path
    ) -> list[CounselAgent]:
    """
    
    """
    start = time.time()
    print("Loading agents...")
    agents = []
    for user in users:
        agents.append(CounselAgent(
            user["name"],
            pipeline,
            user["system_prompt"],
            # path
        ))
    print(f"{len(agents)} agents loaded in {time.time() - start:.2f} seconds.")
    return agents


def main():
    # Initialize a pre-trained pipeline from local storage
    pipe = init_pipeline()

    # Initialize counselor profiles
    counselors = init_counselors()

    # Initialize an agent for each counsil member.
    agents = init_agents(counselors, pipe)

    # Run something 
    print("Starting loop")
    loop_start = time.time()
    n = len(agents)
    for i in range(1):
        start = time.time()
        agent = agents[i % n]
        output = agent.run("What is your name?")
        print("\t", output)
        print(f"Iteration {i}: {time.time() - start:.2f} seconds.")
    print(f"Loop ended in {time.time() - loop_start:.2f} seconds.")

if __name__ == "__main__":
    main()