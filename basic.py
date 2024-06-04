import requests

API_KEY = "sk-AABBCC"
API_URL = "https://api.anthropic.com/v1/complete"

def chat_with_claude(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
         "anthropic-version": "2023-06-01" 
    }
    data = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "model": "claude-v1",
        "max_tokens_to_sample": 100
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["completion"]
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

user_input = input("User: ")
claude_response = chat_with_claude(user_input)
print(f"Assistant: {claude_response}")
