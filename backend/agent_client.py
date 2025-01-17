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
        
    
    def init_secretary_model(self):
        self.secretary = pipeline("summarization", model="Falconsai/text_summarization", max_length=100)


    def init_counselor_model(self):
        self.counselor = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    
    def summarize(self, text: str):
        return self.secretary(text)[0]["summary_text"]
    

    def form_opinion(self,
            setting: str,
            proposal: str,
            personality: str
        ) -> str:
        messages = [
            {
                "role": "system",
                "content": f"{personality} {setting}",
            },
            {
                "role": "user", "content": f"Give your opinion about {proposal}."
            },
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        outputs = outputs[0]["generated_text"]
        opinion = str(outputs).split("<|assistant|>")[-1]
        return opinion
    

    def adjust_opinion(
            self,
            setting: str,
            proposal: str,
            personality: str,
            opinion: str,
            external: str
        ) -> str:
        messages = [
            {
                "role": "system",
                "content": f"{personality} {setting} You are discussing about {proposal} and you opinion about the proposal is as follows: {opinion}",
            },
            {
                "role": "user", "content": f"Adjust your opinion, which is '{opinion}' based on your personality, considering new arguments, which are as follows: {external}"
            },
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        # print(outputs[0]["generated_text"])
        return outputs[0]["generated_text"]
    

    def vote(
            self,
            setting: str,
            proposal: str,
            opinion: str,
            personality: str
        ) -> bool:
        messages = [
            {
                "role": "system",
                "content": f"{personality} {setting}. You are voting about {proposal}. You opinion about this is {opinion}",
            },
            {
                "role": "user", "content": f"Are you for or against {proposal}?"
            },
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=10, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        answer = outputs[0]["generated_text"]
        print(answer)
        return "against" not in answer

# client = AgentClient()
# setting = "You live in a beautiful and thriving city. There is lots of greenery, the people are happy."\
#           "Most people use public transit to move around. You are in a council meeting to discuss and vote about a proposal."
          
# proposal = "leveling the entire city to build a parking lot"
# personality1 = "Your name is Sophia, a 27 year old woman who doesn't own a car. You hate parking lots and want more greenery, like parks, in the city."
# personality2 = "Your name is Marley, a 27 year old man who owns a car. You hate nature and everything about plants and want more space to park your car in the city."
# external = "A recent study has shown that building large parking lots is actually great for the environment. Trees can perfectly grow on them. Furthermore, people actually love watching nature while parked on a parking lot!"
# answers = []
# for personality in [personality1, personality2]:
#     answers.append(client.form_opinion(setting, proposal, personality))
# print(answers, "\n")
# summary = client.summarize(answers[0] + answers[1])
# print(summary)
