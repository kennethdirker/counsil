from pathlib import Path
from typing import Any, Tuple
import time

import torch
from swarms import Agent as SwarmsAgent
from transformers import pipeline, DistilBertForQuestionAnswering, DistilBertTokenizer


# Counselor Agent (DistilBert)
class BertCounselorAgent(SwarmsAgent):
    """
    
    """
    def __init__(
            self, 
            agent_name: str, 
            model: Any,
            tokenizer: Any,
            setting: str,
            proposal: str,
            personality: str,
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

        self.setting: str = setting
        self.proposal: str = proposal
        self.personality: str = personality
        self.opinion: str = ""
        self.vote: bool = None

        super().__init__(
            agent_name = agent_name, 
            *args, 
            **kwargs
        )


    # def extract_arguments(
    #         self,
    #         opinion: str
    #     ) -> str:
    #     """
        
    #     """
    #     question = ""   # TODO
    #     arguments = self.pipeline(
    #         question = question,
    #         context = opinion,
    #         max_length = 100
    #     )["answer"]

    def form_opinion(self) -> str:
        """
        
        """
        context = ...   # TODO personality + setting?
        question = ""   # TODO
        self.opinion = self.pipeline(
            question = question,
            context = context,
            max_length = 100
        )["answer"]

        # TODO some processing?

        return self.opinion


    def adjust_opinion(self, arguments: list[str]) -> Tuple[str, str]:
        """
        Argument
            arguments: List of arguments from other agents/user.
        """
        context = ...   # TODO personality + setting + proposal?
        question = ""   # TODO
        self.opinion = self.pipeline(
            question = question,
            context = context,
            max_length = 100
        )["answer"]

        # TODO some processing?

        return self.opinion


    def vote_accepted(self) -> bool:
        """ 
        Determine whether to accept or reject the proposal based on the
        agent's opinion.

        Argument
            arguments: List of arguments from other agents/user.

        Returns
            True if the agent accepts the proposal, False otherwise.
        """
        context = ...   # TODO personality + setting?
        question = ...  # TODO
        vote = self.pipeline(
            question = question,
            context = context,
            max_length = 1
        )["answer"]

        # TODO some processing?


        if "yes" in vote.lower():   # TODO
            self.vote = True
            return True 
        else:
            self.vote = False
            return False
