import google.generativeai as genai
genai.configure(api_key="Your Key Here")  # replace or load from .env

for model in genai.list_models():
    print(model.name)
