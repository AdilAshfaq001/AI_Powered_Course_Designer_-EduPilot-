import google.generativeai as genai
genai.configure(api_key="AIzaSyDCVtjrfi3thcqmA20PprzX71JtslrfnVQ")  # replace or load from .env

for model in genai.list_models():
    print(model.name)