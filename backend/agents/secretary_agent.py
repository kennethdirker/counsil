# # Standard library imports
# from pathlib import Path
# from typing import Any

# # External imports
# # import torch
# # from swarms import Agent as SwarmsAgent
# from transformers import pipeline

# # class SecretaryAgent:
#     # def __init__(self, id: str, )


# # class BertSecretaryAgent(SwarmsAgent):
# #     """
    
# #     """
# #     def __init__(
# #             self, 
# #             model: Any,
# #             tokenizer: Any,
# #             *args, **kwargs
# #         ):

# #         # Initialize a pre-trained pipeline from local storage
# #         self.pipeline = pipeline(
# #             "question-answering", 
# #             model = model, 
# #             tokenizer = tokenizer,
# #             torch_dtype = torch.bfloat16, 
# #             device_map = "auto"
# #         )
# #         super().__init__(
# #             agent_name = "Secretary", 
# #             *args, 
# #             **kwargs
# #         )


# #     def extract_arguments(
# #             self,
# #             opinions: list[str],
# #             user_input: str = None
# #         ) -> str | list[str]:
# #         """
        
# #         """
# #         arguments = []
# #         question = ""   # TODO
# #         if user_input:
# #             answer = self.pipeline(
# #                 question = question,
# #                 context = user_input,
# #                 max_lenght = 100
# #             )
# #             arguments.append(answer)
        
# #         for context in opinions:
# #             answer = self.pipeline(
# #                 question = question,
# #                 context = context,
# #                 max_lenght = 100
# #             )
# #             arguments.append(answer)

# #         # TODO Do we need to remove duplicate arguments?
        
# #         return arguments