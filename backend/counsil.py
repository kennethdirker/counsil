# Standard library imports
from pathlib import Path
from typing import Any, Tuple
import time

# External imports
# from transformers import pipeline, DistilBertForQuestionAnswering, DistilBertTokenizer

# Package imports
from agents import AgentFactory
from agents.counselor_agent import BertCounselorAgent as Counselor
from agents.secretary_agent import BertSecretaryAgent as Secretary


def init_counselor_profiles():
    """
    Loads the profiles that are used to initialize swarm agents.

    Returns
        List of maps containing the $name and $system_prompt for each counselor.  
    """
    print("Loading counselor profiles...")
    start = time.time()
    users = [{"name": "Karen", "personality": "Your name is Karen and you work as a location manager at McDonalds."}]
    print(f"{len(users)} profiles loaded in {time.time() - start:.2f} seconds.")
    return users


def init_agents(
        profiles: list[dict[str, str]],
        verbose: bool = False        
    ) -> Tuple[list[Counselor], Secretary]:
    """
    
    """
    counselors = []
    start = time.time()
    print("Loading agents...")

    factory = AgentFactory(
        setting = "", # TODO get from db 
        proposal = "",   # TODO get from db
        verbose = True)
    
    # Create counselor agents
    for profile in profiles:
        counselors.append(factory.create_counselor(
            profile["name"], 
            profile["personality"]
        ))

    # Create secretary agent used to extract arguments from counselors
    secretary = factory.create_secretary()

    print(f"{len(counselors) + 1} agents loaded in {time.time() - start:.2f} seconds.")
    return counselors, secretary
