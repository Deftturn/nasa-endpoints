import google.generativeai as genai
# Suppress gRPC logs
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))  # type: ignore


def get_models():    
    models = genai.list_models()  # type: ignore
    model_names = [f"{model.name} - {model.supported_generation_methods}" for model in models]
    return model_names  

def write_to_file(filename: str, data: list):
    with open(filename, 'w') as f:
        for item in data:
            f.write(f"{item}\n")
    print(f"Model names written to {filename}")


def get_and_write_models(filename: str):
    models = get_models()
    write_to_file(filename, models)
    return models

if __name__ == "__main__":
    get_and_write_models("model_names.txt")