# Standard library imports
# from pathlib import Path
# import time

# External imports
import torch
from transformers import pipeline
# from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer


# Package imports
# from counselor_agent import BertCounselorAgent as Counselor
# from secretary_agent import BertSecretaryAgent as Secretary

# DistilBert
class AgentClient:
    def __init__(self, verbose: bool = False):
        """
            verbose: @@@
        """
        self.init_counselor_model()
        self.init_secretary_model()
        # self.setting = setting
        # self.proposal = proposal

        # Load model and tokenizer  
        # model_path = Path("model_bin")
        # model_path /= "TinyLlama-1.1B-Chat-v1.0"
        # start = time.time()
        # if verbose:
        #     print(f"Loading model and tokenizer from {model_path}")
        # self.model = DistilBertForQuestionAnswering.from_pretrained(model_path)
        # self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        # if verbose:
        #     print(f"Model and tokenizer loaded in {time.time() - start:.2f} seconds.")
        
    
    def init_secretary_model(self):
        # model_path = Path("model_bin")
        # model_path /= "text_summarization"
        self.secretary = pipeline("summarization", model="Falconsai/text_summarization")


    def init_counselor_model(self):
        # model_path = Path("model_bin")
        # model_path /= "TinyLlama-1.1B-Chat-v1.0"
        # model = DistilBertForQuestionAnswering.from_pretrained(model_path)
        # tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        # self.counselor = pipeline("text-generation", model=model, tokenizer=tokenizer)
        self.counselor = pipeline("text2text-generation")

    
    def summarize(self, text: str):
        return self.secretary(text)[0]["generated_text"]
    

    def form_opinion(self,
            setting: str,
            proposal: str,
            personality: str
        ) -> str:
        context = "" #TODO setting + proposal + personality
        output = self.counselor(context)
        return output[0]["generated_text"]
    

    def adjust_opinion(
            self,
            setting: str,
            proposal: str,
            personality: str,
            opinion: str,
            external: str
        ) -> str:
        context = "" #TODO setting + proposal + personaliry + agent opinion + external opinions
        output = self.counselor(context)
        return output[0]["generated_text"]
    

    def vote(
            self,
            setting: str,
            proposal: str,
            opinion: str,
        ) -> bool:
        # context = "" #TODO setting + proposal + opinion
        question = f"Answer whether to vote in or reject the proposal '{proposal}' in the setting '{setting}' based on the opinion {opinion}. Answer with yes or no."   #TODO
        output = self.counselor(question)
        if "yes" in output:
            return True
        return False


client = AgentClient()
setting =     "Good evening everyone, thank you for attending tonight's council meeting. "\
               "Our primary agenda item is the zoning of the proposed parking lot on Maple Street. "\
               "As our community grows, so does the need for accessible parking. "\
               "However, it's crucial to balance convenience with environmental impact and neighborhood character. "\
               "Tonight, we'll hear from urban planners, local residents, and business owners to ensure all voices are considered. "\
               "Our goal is to reach a decision that benefits our community as a whole. "\
               "Let's begin by reviewing the proposed zoning changes."
proposal = "We want to level the whole city and build one giant parking lot."
personality = "My name is Sophia, 47 years old. I don't own a car."




    # def create_counselor(self,
    #         name: str,
    #         # personality: str,
    #         *args, **kwargs
    #     ):
    #     """
    #     Arguments
    #         name: Counselor name of agent.
    #         #### personality: Personality and interests of counselor agent.

    #     returns
    #         BertCounselorAgent
    #     """
    #     counselor = Counselor(
    #         agent_name = name,
    #         model = self.model,
    #         tokenizer = self.tokenizer,
    #         # setting = self.setting,
    #         # proposal = self.proposal,
    #         # personality = personality,
    #         *args, **kwargs
    #     )
    #     return counselor
    

    # def create_secretary(self):
    #     """
        
    #     """
    #     secretary = Secretary(self.model, self.tokenizer)
    #     return secretary
