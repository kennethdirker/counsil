from pathlib import Path
from typing import Any
import time

import torch
from swarms import Agent as SwarmsAgent
from transformers import pipeline, DistilBertForQuestionAnswering, DistilBertTokenizer


# Counselor Agent (DistilBert)
class CounselorAgent(SwarmsAgent):
    """
    
    """
    def __init__(
            self, 
            agent_name: str, 
            model: Any,
            tokenizer: Any,
            *args, **kwargs
        ):

        # Initialize a pre-trained pipeline from local storage
        self.pipeline = pipeline(
            "question-answering", 
            model = model, 
            tokenizer = tokenizer,
            torch_dtype = torch.bfloat16, 
            device_map = "auto"
        )
        super().__init__(
            agent_name = agent_name, 
            *args, 
            **kwargs
        )


    def run(self, question: str, context: str) -> str:
        """ Generate text based on the task input. """
        return self.pipeline(
            question = question,
            context = context,
            max_length = 100
        )["answer"]


def init_counselors():
    """
    Loads the profiles that are used to initialize swarm agents.

    Returns
        List of maps containing the $name and $profile for each counselor.  
    """
    start = time.time()
    print("Loading counselor profiles...")
    profile = "There are three people, The first person, Karen, works fulltime at McDonalds. The second person is called Bob. Bob is jobless, but sure does love volenteering at McDonalds. The third person is Heinrich, who works both at McDonalds and CERN."
    users = [
        {"name": "Karen", "profile": profile},
        {"name": "Bob", "profile": profile},
        {"name": "Heinrich", "profile": profile},
    ]
    print(f"{len(users)} profiles loaded in {time.time() - start:.2f} seconds.")
    return users


def init_model():
    start = time.time()
    model_path = Path("model_bin")
    model_path /= "distilbert-base-uncased-distilled-squad"
    print(f"Loading model and tokenizer from {model_path}")
    model = DistilBertForQuestionAnswering.from_pretrained(model_path)
    tokenizer = DistilBertTokenizer.from_pretrained(model_path)
    print(f"Model and tokenizer loaded in {time.time() - start:.2f} seconds.")
    return model, tokenizer


def init_agents(
        users: list[dict[str, str]],
        model: Any,
        tokenizer
    ) -> list[CounselorAgent]:
    """
    
    """
    start = time.time()
    print("Loading agents...")
    agents = []
    for user in users:
        agents.append(CounselorAgent(
            user["name"],
            model,
            tokenizer,
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
        name = counselors[i % n]["name"]
        context = counselors[i % n]["profile"]
        question = f"Can you summarize the text?"
        # question = f"What is the profession of {name}?"
        output = agents[i % n].run(question, context)
        print(f"\tIteration {i}: {time.time() - start:.2f} seconds.", name, output)
    print(f"Loop ended in {time.time() - loop_start:.2f} seconds.")


if __name__ == "__main__":
    main()