# Standard library imports
from pathlib import Path
import time

# External imports
from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer


# Package imports
from counselor_agent import BertCounselorAgent as Counselor
from secretary_agent import BertSecretaryAgent as Secretary

# DistilBert
class AgentFactory:
    def __init__(
            self, 
            setting: str,
            proposal: str,
            verbose: bool = False
        ):
        """
        Arguments
            model_path: @@@
            setting: Description of the city.
            proposal: @@@
            verbose: @@@
        """
        self.setting = setting
        self.proposal = proposal

        # Load model and tokenizer  
        model_path = Path("model_bin")
        model_path /= "TinyLlama-1.1B-Chat-v1.0"
        start = time.time()
        if verbose:
            print(f"Loading model and tokenizer from {model_path}")
        self.model = DistilBertForQuestionAnswering.from_pretrained(model_path)
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        if verbose:
            print(f"Model and tokenizer loaded in {time.time() - start:.2f} seconds.")
        



    def create_counselor(self,
            name: str,
            personality: str,
            *args, **kwargs
        ):
        """
        Arguments
            name: Counselor name of agent.
            personality: Personality and interests of counselor agent.

        returns
            BertCounselorAgent
        """
        counselor = Counselor(
            agent_name = name,
            model = self.model,
            tokenizer = self.tokenizer,
            setting = self.setting,
            proposal = self.proposal,
            personality = personality,
            *args, **kwargs
        )
        return counselor
    

    def create_secretary(self):
        """
        
        """
        secretary = Secretary(self.model, self.tokenizer)
        return secretary
