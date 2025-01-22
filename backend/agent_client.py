# Standard library imports
from pathlib import Path
import os


# External imports
import torch
from transformers import pipeline

# DistilBert
class AgentClient:
    def __init__(self):
        self.init_counselor_model()
        self.init_secretary_model()
        
    
    def init_secretary_model(self):
        self.secretary = pipeline("summarization", model="Falconsai/text_summarization", max_length=100)


    def init_counselor_model(self):
        # model_path = Path("backend", "agents", "model_bin")
        # model_path /= "TinyLlama-1.1B-Chat-v1.0"
        # if model_path.is_dir():
        #     # Load from local storage
        #     print("Loading counselor model from local storage")
        #     model = AutoModel.from_pretrained(model_path)
        #     tokenizer = AutoTokenizer.from_pretrained(model_path)
        #     self.counselor = pipeline("text-generation", model=model, tokenizer=tokenizer)
        # else:
        #     # Load from remote
        #     print("Loading counselor model from remote")
        #     self.counselor = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.counselor = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    
    def summarize(self, text: str):
        return self.secretary(text)[0]["summary_text"]
    

    def form_opinion(self,
            proposal: str,
            personality: str
        ) -> str:
        """ Form an inital viewpoint based on a proposal and counselor personality. """
        messages = [
            {
                "role": "system",
                "content": f"{personality}",
            },
            {
                "role": "user", 
                "content": f"The chairman of has opened the meeting by saying the following: '{proposal}'."                 
            },
            {
                "role": "user",
                "content": f"What is your opinion about the proposal in the opening talk by the city council chairman?"
            }
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        outputs = outputs[0]["generated_text"]
        opinion = str(outputs).split("<|assistant|>")[-1]
        return opinion
    

    def adjust_opinion(
            self,
            proposal: str,
            personality: str,
            opinion: str,
            external: str
        ) -> str:
        """ Adjust the current viewpoint according to arguments from other agents. """
        messages = [
            {
                "role": "system",
                "content": f"{personality}",
            },
            {
                "role": "system", 
                "content": f"The chairman of has opened the meeting by saying the following: '{proposal}'."                 
            },
            {
                "role": "user",
                "content": f"What is your opinion about the proposal in the opening talk by the city council chairman?"
            },
            {
                "role": "assistant",
                "content": opinion
            },
            {
                "role": "user",
                "content": f"A summarization of the opinions of the other counselors in the meeting is as follow: '{external}'. Write an opinion about their viewpoints."
            }
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        outputs = outputs[0]["generated_text"]
        opinion = str(outputs).split("<|assistant|>")[-1]
        return opinion
    

    def vote(
            self,
            proposal: str,
            opinion: str,
            personality: str
        ) -> bool:
        """ Vote to accept or reject a proposal based on the persona and viewpoint of a counselor. """
        messages = [
            {
                "role": "system",
                "content": f"{personality}",
            },
            {
                "role": "user", 
                "content": f"The chairman of has opened the meeting by saying the following: '{proposal}'."                 
            },
            {
                "role": "user",
                "content": f"What is your opinion about the proposal in the opening talk by the city council chairman?"
            },
            {
                "role": "assistant",
                "content": opinion
            },
            {
                "role": "user",
                "content": "Considering your opinion and personality, do you vote in favor or against the proposal that was introduced by the city council chairman?"
            }
        ]
        prompt = self.counselor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        outputs = self.counselor(prompt, max_new_tokens=10, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        outputs = outputs[0]["generated_text"]
        answer = str(outputs).split("<|assistant|>")[-1]
        print(answer)
        return "against" not in answer