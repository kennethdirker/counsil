import argparse, os
from pathlib import Path

# External libs
import torch
from transformers import AutoModelForCausalLM


def main(model_id: str, save_name: str):
    torch.random.manual_seed(0)
    print("Downloading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype = "auto",
        trust_remote_code = True        
    )

    # Create model bin directory
    save_path = Path("model_bin")
    if save_path.exists():
        if not save_path.is_dir():
            raise Exception("Can't make directory 'model_bin': Name already taken!")
    else:
        os.mkdir(save_path)

    # Create free save path for directory
    save_path /= str(save_name)
    if save_path.exists():
        i = 0
        while Path(str(save_path) + str(i)).exists():
             i += 1
        save_path = Path(str(save_path) + str(i))
    print("Saving model to:", save_path)
    model.save_pretrained(save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model")
    args = parser.parse_args()
    model_id = str.split(args.model, "/")
    print(f"Model ID: {args.model}")
    main(args.model, model_id[-1])


