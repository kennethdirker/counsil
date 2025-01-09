from pathlib import Path

# External libs
import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, DistilBertForQuestionAnswering, DistilBertTokenizer

# Download model from Huggingface
# pipe = pipeline("distilbert/distilbert-base-uncased-distilled-squad")

# OR

# Load local model
path = Path("model_bin")
path /= "distilbert-base-uncased-distilled-squad"
model = DistilBertForQuestionAnswering.from_pretrained(path)
tokenizer = DistilBertTokenizer.from_pretrained(path)
pipe = pipeline(    
    "question-answering", 
    model = model, 
    tokenizer = tokenizer
)

res = pipe(context="Your name is Karen", question="what is your name?")
print(res)
res = pipe(question="can bees fly?", context="Scientists tell us that it is impossible for bees to fly, according to the tiny wing sizes bees have compared to their heavy body. The bee, of course, doesn't care about science and flies anyways.")
print(res)
