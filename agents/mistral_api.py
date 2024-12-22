from mistralai import Mistral

api_key = "29c5RhZzenjfWkIwtR3GR4JHoojKpl8L"
model = "mistral-large-latest"
client = Mistral(api_key=api_key)

# https://github.com/mistralai/cookbook/blob/main/mistral/agents/conversation_agent.ipynb
# https://docs.mistral.ai/capabilities/agents/
# https://github.com/mistralai/cookbook/blob/main/mistral/prompting/prompting_capabilities.ipynb

done = False
print(f"Talking to {model}. Type exit to exit.")
while not done:
    text = input("Input:\n\t")
    if text == "exit":
        break
   
    response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": text
            }
        ] 
    )
    print(response.choices[0].message.content)