from mistralai import Mistral
import os

# GLOBAL
api_key = os.getenv("MISTRAL_API_KEY")
# model = "mistral-large-latest"
model = "open-mistral-nemo"
client = Mistral(api_key=api_key)

# https://github.com/mistralai/cookbook/blob/main/mistral/agents/conversation_agent.ipynb
# https://docs.mistral.ai/capabilities/agents/
# https://github.com/mistralai/cookbook/blob/main/mistral/prompting/prompting_capabilities.ipynb


def ask(user: str, text: str, log: dict) -> str:
    log[user].append(
        {
            "role": "user",
            "content": text
        }
    )

    response = client.chat.complete(
        model = model,
        messages = log[user]
    )

    answer = response.choices[0].message.content
    log[user].append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    return answer

def set_personality(user, text: str, log: dict) -> str:
    """ Adjust the personality of an agent. """
    log[user].append(
        {
            "role": "system",
            "content": text
        }
    )

    response = client.chat.complete(
        model = model,
        messages = log[user]
    )

    answer = response.choices[0].message.content
    log[user].append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    return answer


def init(names: list) -> dict[str, list[dict[str, str]]]:
    """ Create personalities log. """
    log = {}
    for name in names:
        log[name] = []
        set_personality(name, f"Your name is {name}", log)
    return log

def main():
    print("Talking to", model)
    users = ["Karen", "Chad", "Kevin"]
    log = init(users)
    i = 0
    current_user = users[i % len(users)]
    done = False

    while not done:
        # Get input
        text = input(f"Ask {current_user} something or type 'exit':\n\t")
        if text == "exit":
            break
        answer = ask(current_user, text, log)
        print(answer)
        i += 1
        current_user = users[i % len(users)]
    


if __name__ == "__main__":
    main()